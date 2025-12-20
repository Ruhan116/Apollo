# Goals Service

AI-Powered Goal Management microservice using **Gemini 2.5 Flash** and the Harada Method.

## Features

- AI-powered goal breakdown using Gemini 2.5 Flash
- Harada Method: Goals → Subgoals → Action Steps
- Automatic categorization (Skill, Mental, Communication)
- 6-8 subgoals per goal
- 6-8 action steps per subgoal
- Circuit breaker for AI API calls
- Full observability (logging, tracing, metrics)

## Endpoints

### Goals Endpoints
- `POST /goals/create` - Create AI-powered goal breakdown

### Health Checks
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe (checks DB + Gemini API)
- `GET /metrics` - Prometheus metrics

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and configure:
   - Set `GEMINI_API_KEY`
   - Set `DATABASE_URL`

3. Run the service:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

4. Access documentation: http://localhost:8002/docs

## AI Model

Uses **Gemini 2.5 Flash** for fast, efficient goal planning.

## Example Request

```json
POST /goals/create
{
  "user_id": 1,
  "prompt": "I want to learn Python programming"
}
```

## Environment Variables

See `.env.example` for all configuration options.
