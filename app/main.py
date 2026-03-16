from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="RoboAdviser Demo API",
    description=(
        "Efficient Frontier based asset allocation simulation API for demo and research use. "
        "This service is not investment advice."
    ),
    version="0.1.0",
)

app.include_router(router)
