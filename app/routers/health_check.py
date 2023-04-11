from fastapi import APIRouter

router = APIRouter(tags=['health check'])


@router.get("/ping")
def ping() -> dict[str, str]:
    """Endpoint for checking if the API is accessible"""
    return {"ping": "pong!"}
