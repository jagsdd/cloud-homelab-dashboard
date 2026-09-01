from prometheus_client import Counter

servers_created_total = Counter(
    "servers_created_total",
    "Total number of servers created"
)

