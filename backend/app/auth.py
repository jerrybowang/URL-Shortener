import requests
import httpx
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from app.config import AUTH0_DOMAIN, API_AUDIENCE, M2M_CLIENT_ID, M2M_CLIENT_SECRET
from app.models import LinkRequest

reusable_oauth2 = HTTPBearer()

# (Optional) simple caching to avoid requesting every time
jwks_cache = None
management_api_token = None


def get_jwks() -> dict:
    global jwks_cache
    if jwks_cache is None:
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        response = requests.get(jwks_url)
        jwks_cache = response.json()
    return jwks_cache


def get_management_api_token() -> str:
    global management_api_token
    if management_api_token:
        decoded_token = jwt.get_unverified_claims(management_api_token)
        expires_at = datetime.fromtimestamp(decoded_token["exp"]).replace(
            tzinfo=timezone.utc
        )
        if expires_at > datetime.now(timezone.utc) + timedelta(seconds=10):
            return management_api_token

    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": M2M_CLIENT_ID,
        "client_secret": M2M_CLIENT_SECRET,
        "audience": API_AUDIENCE,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    management_api_token = response.json()["access_token"]
    return management_api_token


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


def verify_token(token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)):
    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token.credentials)
        rsa_key = {}
        alg = ["RS256"]
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                alg = key.get("alg", ["RS256"])  # fallback to RS256 if alg not set
        if rsa_key:
            payload = jwt.decode(
                token.credentials,
                rsa_key,
                algorithms=[].extend(alg),
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

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
