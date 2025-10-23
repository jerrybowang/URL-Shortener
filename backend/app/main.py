from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.auth import verify_token
from app.models import URLRequest

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


@app.post("/shorten")
def protected(data: URLRequest, user=Depends(verify_token)):
    return {"short_url": "https://not-yet-implemented"}
