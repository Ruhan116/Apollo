# Auth Service

Authentication and Authorization microservice for Apollo platform.

## Features

- User registration and login
- JWT token generation and verification
- Password hashing with bcrypt
- Email and password validation
- Service-to-service authentication

## Endpoints

### Public Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Service Endpoints (require service key)
- `POST /auth/verify` - Verify JWT token
- `GET /auth/user/{user_id}` - Get user by ID

### Health Checks
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe
- `GET /metrics` - Prometheus metrics

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and configure

3. Run the service:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

4. Access documentation: http://localhost:8001/docs

## Environment Variables

See `.env.example` for all configuration options.
