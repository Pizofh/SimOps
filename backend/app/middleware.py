from __future__ import annotations

import logging
from time import perf_counter
from uuid import uuid4

from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.logging_config import reset_request_id, set_request_id
from app.metrics import ERRORS_TOTAL, HTTP_REQUEST_DURATION_SECONDS, HTTP_REQUESTS_TOTAL

logger = logging.getLogger(__name__)


def resolve_route_path(scope: Scope) -> str:
    route = scope.get("route")

    if route is not None and hasattr(route, "path"):
        return route.path

    return scope.get("path", "unknown")


class ObservabilityMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        request_id = headers.get("x-request-id", str(uuid4()))
        method = scope["method"]
        start_time = perf_counter()
        status_code = 500
        token = set_request_id(request_id)

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]
                mutable_headers = MutableHeaders(scope=message)
                mutable_headers["X-Request-ID"] = request_id

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception:
            ERRORS_TOTAL.labels(category="request_exception").inc()
            logger.exception(
                "request_failed",
                extra={
                    "extra_fields": {
                        "method": method,
                        "path": resolve_route_path(scope),
                    }
                },
            )
            raise
        finally:
            path = resolve_route_path(scope)
            duration_seconds = perf_counter() - start_time

            HTTP_REQUESTS_TOTAL.labels(
                method=method,
                path=path,
                status_code=str(status_code),
            ).inc()
            HTTP_REQUEST_DURATION_SECONDS.labels(method=method, path=path).observe(
                duration_seconds
            )

            if status_code >= 500:
                ERRORS_TOTAL.labels(category="http_5xx").inc()

            logger.info(
                "request_completed",
                extra={
                    "extra_fields": {
                        "method": method,
                        "path": path,
                        "status_code": status_code,
                        "duration_ms": round(duration_seconds * 1000, 2),
                    }
                },
            )
            reset_request_id(token)


class SecurityHeadersMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers["X-Content-Type-Options"] = "nosniff"
                headers["X-Frame-Options"] = "DENY"
                headers["Referrer-Policy"] = "no-referrer"

            await send(message)

        await self.app(scope, receive, send_wrapper)
