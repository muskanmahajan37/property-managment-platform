from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.flex.auth import auth_api
from src.flex.core.config import get_settings
from src.flex.property.api import api_router as property_api
from src.flex.user.api import api_router as user_api


def get_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(**settings.fastapi_kwargs)
    return app


app = get_app()
public_router = APIRouter()

public_router.include_router(auth_api, prefix="", tags=["Auth"])
public_router.include_router(user_api, prefix="/users", tags=["User"])
public_router.include_router(property_api, prefix="/properties", tags=["Properties"])

api_router = APIRouter()
api_router.include_router(public_router)

app.include_router(api_router, prefix=get_settings().API_PREFIX)
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
