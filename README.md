# URL-Shortener

This is a **practice project** focusing primarily on **backend development**.  
The frontend is a **minimal React web app**, generated with AI, serving mainly as a testing interface.



## Overview

- **Authentication:** Handled via **Auth0**.  
- **Authorization:** The frontend passes a **JWT** to the backend, which verifies it before processing requests.
- **Frontend:** Simple React app to interact with the backend API.
- **Backend:** Containerized API service for authentication and request handling.
- **Secrets:**
 `.env` for local development, secrets management(eg. Github secrets) for CI/CD and cloud environment.

## Setup Instructions

### 1. Create a `.env` File

Create a `.env` file in the project root directory with the following environment variables:

```bash
REACT_APP_AUTH0_DOMAIN=<your_auth0_domain>
REACT_APP_AUTH0_CLIENT_ID=<your_auth0_client_id>
REACT_APP_AUTH0_API_AUDIENCE=<your_auth0_api_audience>

AUTH0_DOMAIN=<your_auth0_domain>
API_AUDIENCE=<your_auth0_api_audience>
```

The `REACT_APP_` variables are used by the frontend (React),
while `AUTH0_DOMAIN` and `API_AUDIENCE` are used by the backend.

### 2. Start the Services

To spin up both the frontend and backend using Docker Compose.

```bash
docker compose up
```

Ingress simulation is obmitted for now due to complex configs.


## Notes

- Make sure your Auth0 configuration matches the frontend callback URLs and API audience.

- If you encounter `Invalid audience` or `Unauthorized` errors, verify that your `.env` values are consistent between frontend and backend.

- This project is for learning and experimentation — not production use.