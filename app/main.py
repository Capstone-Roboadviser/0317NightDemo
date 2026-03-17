from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import APP_DESCRIPTION, APP_NAME, APP_VERSION


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)

app.include_router(api_router)
