from fastapi import APIRouter
from app.api.routes import settlement

api_router = APIRouter()
api_router.include_router(settlement.router)
