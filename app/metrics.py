from prometheus_client import Counter, Histogram

servers_created_total = Counter(
    "servers_created_total",
    "Total number of servers created"
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds"
)
