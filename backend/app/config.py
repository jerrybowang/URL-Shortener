import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into os.environ

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
