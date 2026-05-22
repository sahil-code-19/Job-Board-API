import time
import logging

from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("app.middleware.request")

class RequestLoggingMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        try:
            redis = request.app.state.redis
            await redis.incr("metrics:total_requests") 
            await redis.incrbyfloat("metrics:total_latency_ms", process_time)
            if response.status_code >= 400:
                await redis.incr("metrics:total_errors")
        except Exception:
            pass

        logger.info(
            f"{request.method} {request.url.path}"
            f"Status {response.status_code}"
            f"Time: {process_time:.4f}"
            f"Client: {request.client.host}"
            f"Request ID: {request.state.request_id}"
        )
        return response