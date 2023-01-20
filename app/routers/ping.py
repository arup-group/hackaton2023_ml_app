from fastapi import APIRouter
router = APIRouter(prefix="/ping")


@router.get("/", tags=["Ping"], response_model=str)
async def request_pong() -> str:
    return "Hackaton 2023 is awesome! Thank you all! <3"
