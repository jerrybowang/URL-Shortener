# URL-Shortener

This is a **practice project** focusing primarily on **backend development**.  
The frontend is a **minimal React web app**, generated with AI, serving mainly as a testing interface.



## Overview

- **Authentication:** Handled via **Auth0**.  
- **Authorization:** The frontend passes a **JWT** to the backend, which verifies it before processing requests.
- **Frontend:** Simple React app to interact with the backend API.
- **Backend:** Containerized API service for request handling.
- **Secrets:**
 `.env` for local development, secrets management(eg. Github secrets) for CI/CD and cloud environment.

## Setup Instructions

### 1. Create a `.env` File

Create a `.env` file in the project root directory with the following environment variables:

```bash
# used by the frontend (React)
REACT_APP_AUTH0_DOMAIN=< your auth0 domain >
REACT_APP_AUTH0_CLIENT_ID=< your auth0 client ID >
REACT_APP_AUTH0_API_AUDIENCE=< your auth0 api audience >

# used by the backend
AUTH0_DOMAIN=< your auth0 domain >
API_AUDIENCE=< your auth0 api audience >

# used by the DB
POSTGRES_USER=< user name >
POSTGRES_PASSWORD=< secret password >
POSTGRES_DB=< DB name >
POSTGRES_HOST=< must matches the service name in docker-compose >
POSTGRES_PORT=< port number >
DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}


```

### 2. Start the Services

To spin up the service using Docker Compose.

```bash
docker compose up
```

Ingress simulation is obmitted for now due to complex configs.


## Notes

- Make sure your Auth0 configuration matches the frontend callback URLs and API audience.

- If you encounter `Invalid audience` or `Unauthorized` errors, verify that your `.env` values are consistent between frontend and backend.

- This project is for learning and experimentation — not production use.