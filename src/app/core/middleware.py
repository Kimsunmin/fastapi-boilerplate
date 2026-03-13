import re
import time
from uuid import uuid4

from fastapi import Request
from loguru import logger


EXCLUDE_PATHS = {
    "/docs",
    # "/openapi.json",
    "/redoc",
}


async def log_requests(request: Request, call_next):
    path = request.url.path

    if any(path.startswith(prefix) for prefix in EXCLUDE_PATHS):
        return await call_next(request)

    start_time = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start_time) * 1000

    status_code = response.status_code
    client_ip = request.client.host if request.client else "unknown"

    if status_code >= 500:
        status_color = "red"
    elif status_code >= 400:
        status_color = "yellow"
    else:
        status_color = "green"

    message = (
        "[Request ID: <magenta>{}</magenta>] "
        "<blue>{}</blue> | "
        "<cyan>{}</cyan> {} "
        f"<{status_color}>{{}}</{status_color}> | "
        "<green>{:.2f} ms</green>"
    )

    if status_code >= 500:
        logger.opt(colors=True).error(
            message,
            request.state.request_id,
            client_ip,
            request.method,
            path,
            status_code,
            duration,
        )
    elif status_code >= 400:
        logger.opt(colors=True).warning(
            message,
            request.state.request_id,
            client_ip,
            request.method,
            path,
            status_code,
            duration,
        )
    else:
        logger.opt(colors=True).info(
            message,
            request.state.request_id,
            client_ip,
            request.method,
            path,
            status_code,
            duration,
        )

    return response

async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID")

    if not request_id:
        request_id = str(uuid4())
        
    request.state.request_id = request_id
    response = await call_next(request)
    
    response.headers["X-Request-ID"] = request_id
    return response