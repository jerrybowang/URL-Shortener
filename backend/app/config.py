import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into os.environ

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
M2M_CLIENT_ID = os.environ["M2M_CLIENT_ID"]
M2M_CLIENT_SECRET = os.environ["M2M_CLIENT_SECRET"]
