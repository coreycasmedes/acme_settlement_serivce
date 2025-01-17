from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
