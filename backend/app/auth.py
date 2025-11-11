import asyncio
import httpx
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from app.config import AUTH0_DOMAIN, API_AUDIENCE, M2M_CLIENT_ID, M2M_CLIENT_SECRET
from app.models import LinkRequest

reusable_oauth2 = HTTPBearer()
JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"

# Cache + Locks
_jwks_cache = None
_jwks_expire_at = datetime.min.replace(tzinfo=timezone.utc)
_jwks_lock = asyncio.Lock()

_management_token = None
_management_token_expire_at = datetime.min.replace(tzinfo=timezone.utc)
_management_lock = asyncio.Lock()


async def get_jwks() -> dict:
    global _jwks_cache, _jwks_expire_at
    now = datetime.now(timezone.utc)
    if _jwks_cache and now < _jwks_expire_at:
        return _jwks_cache

    # case: cache miss
    async with _jwks_lock:
        # double check
        if _jwks_cache and now < _jwks_expire_at:
            return _jwks_cache

        async with httpx.AsyncClient() as client:
            response = await client.get(JWKS_URL, timeout=10)
            response.raise_for_status()
            jwks = response.json()

        _jwks_cache = jwks
        _jwks_expire_at = now + timedelta(hours=10)  # 10 hours

    return jwks


async def get_management_api_token() -> str:
    global _management_token, _management_token_expire_at

    now = datetime.now(timezone.utc)

    if _management_token and now < _management_token_expire_at - timedelta(seconds=60):
        return _management_token

    # case: cache miss
    async with _management_lock:
        # double check
        if _management_token and now < _management_token_expire_at - timedelta(
            seconds=60
        ):
            return _management_token

        payload = {
            "grant_type": "client_credentials",
            "client_id": M2M_CLIENT_ID,
            "client_secret": M2M_CLIENT_SECRET,
            "audience": API_AUDIENCE,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(TOKEN_URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

        token = data["access_token"]
        claims = jwt.get_unverified_claims(token)
        exp = datetime.fromtimestamp(claims["exp"], tz=timezone.utc)

        _management_token = token
        _management_token_expire_at = exp

        return token


async def link_account_helper(data: LinkRequest, token):
    async with httpx.AsyncClient() as client:
        body = {"provider": data.provider, "user_id": data.secondary_user_id}
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = await client.post(
            f"https://{AUTH0_DOMAIN}/api/v2/users/{data.primary_user_id}/identities",
            headers=header,
            json=body,
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


async def verify_token(token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)):
    try:
        jwks = await get_jwks()
        unverified_header = jwt.get_unverified_header(token.credentials)

        rsa_key = None
        for key in jwks["keys"]:
            if key["kid"] == unverified_header.get("kid"):
                rsa_key = key
                break

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid header: key ID not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        payload = jwt.decode(
            token.credentials,
            rsa_key,
            algorithms=[rsa_key.get("alg", "RS256")],
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
