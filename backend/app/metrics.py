from prometheus_client import Counter, Gauge, Histogram

TOTAL_EVENTS_RECEIVED = Counter(
    "total_events_received",
    "Total number of events successfully received by the backend.",
)
TOTAL_EVENTS_BY_SEVERITY = Counter(
    "total_events_by_severity",
    "Total number of received events by severity.",
    labelnames=("severity",),
)
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests handled by the backend.",
    labelnames=("method", "path", "status_code"),
)
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds.",
    labelnames=("method", "path"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)
BACKEND_UP = Gauge(
    "backend_up",
    "Backend process availability.",
)
ERRORS_TOTAL = Counter(
    "errors_total",
    "Total number of error conditions observed by the backend.",
    labelnames=("category",),
)


def record_event_ingested(severity: str) -> None:
    TOTAL_EVENTS_RECEIVED.inc()
    TOTAL_EVENTS_BY_SEVERITY.labels(severity=severity).inc()

    if severity in {"error", "timeout"}:
        ERRORS_TOTAL.labels(category=f"event_{severity}").inc()

