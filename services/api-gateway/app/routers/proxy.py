"""Proxy router for forwarding requests to backend services"""
import httpx
from fastapi import APIRouter, Request, Response, HTTPException
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


# Service routing map
SERVICE_MAP = {
    "/api/auth": settings.AUTH_SERVICE_URL,
    "/api/goals": settings.GOALS_SERVICE_URL,
}

SERVICE_API_KEYS = {
    settings.AUTH_SERVICE_URL: settings.AUTH_SERVICE_API_KEY,
    settings.GOALS_SERVICE_URL: settings.GOALS_SERVICE_API_KEY,
}


async def proxy_request(request: Request, service_url: str, path: str) -> Response:
    """
    Proxy request to backend service

    Args:
        request: Incoming FastAPI request
        service_url: Base URL of the backend service
        path: Path to forward to the service

    Returns:
        Response from the backend service
    """
    # Build full URL
    target_url = f"{service_url}{path}"
    if request.url.query:
        target_url += f"?{request.url.query}"

    # Prepare headers
    headers = dict(request.headers)

    # Remove host header to avoid conflicts
    headers.pop("host", None)

    # Add correlation ID
    if hasattr(request.state, "correlation_id"):
        headers["X-Correlation-ID"] = request.state.correlation_id

    # Add user ID for authenticated requests
    if hasattr(request.state, "user_id"):
        headers["X-User-ID"] = str(request.state.user_id)
        headers["X-User-Email"] = request.state.email

    # Add service API key for service-to-service auth
    service_api_key = SERVICE_API_KEYS.get(service_url)
    if service_api_key:
        headers["X-Service-Key"] = service_api_key

    # Get request body
    body = await request.body()

    try:
        async with httpx.AsyncClient() as client:
            # Forward request to backend service
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=30.0
            )

            # Return response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )

    except httpx.TimeoutException:
        logger.error(f"Timeout proxying request to {target_url}")
        raise HTTPException(status_code=504, detail="Gateway timeout")
    except httpx.RequestError as e:
        logger.error(f"Error proxying request to {target_url}: {str(e)}")
        raise HTTPException(status_code=502, detail="Bad gateway")


@router.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    """
    Main proxy endpoint - routes requests to appropriate backend services
    """
    # Determine which service to route to
    full_path = f"/api/{path}"

    # Find matching service
    service_url = None
    service_path = None

    for prefix, url in SERVICE_MAP.items():
        if full_path.startswith(prefix):
            service_url = url
            # Remove the /api prefix and the service prefix
            service_path = full_path.replace("/api", "")
            break

    if not service_url:
        raise HTTPException(status_code=404, detail="Service not found")

    logger.info(
        f"Proxying {request.method} {full_path} to {service_url}{service_path}",
        extra={
            "extra_fields": {
                "method": request.method,
                "path": full_path,
                "target": f"{service_url}{service_path}"
            }
        }
    )

    return await proxy_request(request, service_url, service_path)
