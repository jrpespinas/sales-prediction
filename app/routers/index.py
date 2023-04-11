from fastapi import APIRouter

router = APIRouter(tags=['home'])


@router.get("/")
def index() -> dict[str, str]:
    """Landing endpoint of the API"""
    return {"message": "Hello, world!"}
