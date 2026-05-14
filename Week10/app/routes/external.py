import pybreaker
from fastapi import APIRouter, HTTPException, status

from app.core.circuit_breaker import fetch_recommendation_from_external_service, recommendation_breaker

router = APIRouter(prefix="/external", tags=["external service"])


@router.get("/recommendation")
def get_recommendation():
    try:
        result = fetch_recommendation_from_external_service()
        return {
            "status": "success",
            "circuit_state": recommendation_breaker.current_state,
            "data": result,
        }
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Circuit breaker is open. External recommendation service is blocked temporarily.",
        )
    except ConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
