from fastapi import FastAPI, Depends, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# import DB libs
from sqlalchemy import inspect
from sqlalchemy.orm import Session

# import DB and models
from app.DB.database import engine, get_db
from app.DB.models import URL

# import helpers
from app.auth import verify_token
from app.models import URLRequest
from app.utils import hash_64, add_entry_to_db

app = FastAPI()


# allow frontend dev server
origins = [
    "http://localhost:3000",  # your frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # allow Authorization header
)

@app.get("/")
def public():
    return {"message": "Welcome to the public API!"}

@app.get("/api/health")
def health():
    return {"message": "I'm alive!"}

@app.get("/debug/schema")
def debug_schema():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    schema_info = {}
    for table in tables:
        columns = [
            {
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col["nullable"],
                "default": str(col["default"]),
            }
            for col in inspector.get_columns(table)
        ]
        schema_info[table] = columns

    return schema_info


@app.get("/{key}")
def get_long_url(key: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_key == key).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    return RedirectResponse(url_entry.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.post("/shorten/custom")
def shorten_custom(data: URLRequest, overwrite: bool, user=Depends(verify_token)):
    alias = data.custom_alias
    '''
    if alias in db:
        record = db[alias]
        if record["owner"] != user["sub"]:  # other's alias
            raise HTTPException(status_code=409, detail="Alias already taken")
        elif not overwrite:
            # own alias, but havn't state overwrite
            raise HTTPException(
                status_code=409,
                detail={"message": "Alias exists but owned by you", "can_overwrite": True}
            )

    '''
    if alias:
        return {"short_url": f"https://not-yet-implemented/{alias}"}
    else:
        return {"short_url": "https://not-yet-implemented/regular-short"}


@app.post("/shorten")
def shorten(data: URLRequest, request: Request, db: Session = Depends(get_db)):
    # check if url already exists
    long_url_hash = hash_64(data.long_url)
    url_entry = db.query(URL).filter(URL.long_url_hash == long_url_hash).first()
    if url_entry:
        short_url = str(request.url_for("get_long_url", key=url_entry.short_key))
        return {"short_url": short_url}
    
    # case: need to construct the entry
    key = add_entry_to_db(data.long_url, db)

    # return the short url
    short_url = str(request.url_for("get_long_url", key=key))
    return {"short_url": short_url}

    
