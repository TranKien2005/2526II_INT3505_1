import random
import time

import pybreaker

recommendation_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=20)


@recommendation_breaker
def fetch_recommendation_from_external_service() -> dict[str, str]:
    time.sleep(0.1)
    if random.random() < 0.45:
        raise ConnectionError("Recommendation service is temporarily unavailable")
    return {
        "book": "Clean Architecture",
        "reason": "Phu hop de hoc cach thiet ke API va he thong production.",
    }
