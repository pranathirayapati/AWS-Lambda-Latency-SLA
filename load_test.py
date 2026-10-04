import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://cvc9koonuf.execute-api.eu-north-1.amazonaws.com"

SLA = 300
REQUESTS = 100
WORKERS = 2


def send_request(url):
    start = time.perf_counter()

    try:
        response = requests.post(
            url,
            json={"amount": 1500},
            timeout=10
        )

        latency = (time.perf_counter() - start) * 1000
        return response.status_code, latency

    except Exception:
        return 500, 10000


def percentile(values, p):
    values = sorted(values)
    index = int(len(values) * p / 100)

    if index >= len(values):
        index = len(values) - 1

    return values[index]


def test(name, url):

    print("\nTesting:", name)

    results = []

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:

        futures = [
            executor.submit(send_request, url)
            for _ in range(REQUESTS)
        ]

        for future in as_completed(futures):
            results.append(future.result())

    latencies = [x[1] for x in results]

    successful = [
        x for x in results
        if x[0] == 200
    ]

    sla_count = sum(
        1
        for x in successful
        if x[1] <= SLA
    )

    print("Requests:", len(results))
    print("Successful:", len(successful))

    print(
        "Average:",
        round(statistics.mean(latencies), 2),
        "ms"
    )

    print(
        "P95:",
        round(percentile(latencies, 95), 2),
        "ms"
    )

    print(
        "P99:",
        round(percentile(latencies, 99), 2),
        "ms"
    )

    print(
        "SLA Compliance:",
        round(
            sla_count / REQUESTS * 100,
            2
        ),
        "%"
    )


test(
    "BASELINE",
    BASE_URL + "/baseline"
)

test(
    "PROVISIONED CONCURRENCY",
    BASE_URL + "/optimized"
)