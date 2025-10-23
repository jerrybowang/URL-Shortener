# --- Frontend Dockerfile ---
FROM node:24-alpine

WORKDIR /app

RUN npx create-react-app . --template cra-template-pwa
RUN npm install @auth0/auth0-react axios

COPY /src /app/src

# Development mode (will override CMD in docker-compose)
CMD ["npm", "start"]
