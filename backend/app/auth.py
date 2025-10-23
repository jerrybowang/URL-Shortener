import json
from jose import jwt, JWTError, ExpiredSignatureError
from urllib.request import urlopen
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import AUTH0_DOMAIN, API_AUDIENCE

reusable_oauth2 = HTTPBearer()

# (Optional) simple caching to avoid downloading JWKS every time
jwks_cache = None

def get_jwks():
    global jwks_cache
    if jwks_cache is None:
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        with urlopen(jwks_url) as response:
            jwks_cache = json.load(response)
    return jwks_cache


def verify_token(token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)):
    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token.credentials)
        rsa_key = {}
        alg = "RS256"
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                alg = key.get("alg", "RS256")  # fallback to RS256 if alg not set
        if rsa_key:
            payload = jwt.decode(
                token.credentials,
                rsa_key,
                algorithms=[alg],
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
