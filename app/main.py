from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .core.config_loader import settings
from fastapi.exceptions import RequestValidationError
from app.utils.exception_utils import validation_exception_handler
from app.modules.auth.routes.auth_router import auth_router
from app.modules.user.routes.user_router import user_router

openapi_tags = [
    {"name": "Health Checks", "description": "Application health checks"},
    {"name": "Auth", "description": "Authentication"},
    {"name": "Users", "description": "User management"},
]

app = FastAPI(title="SitenSight API", openapi_tags=openapi_tags)

if settings.BACKEND_CORS_ORIGINS:
    origins = [o.strip() for o in settings.BACKEND_CORS_ORIGINS.split(",") if o.strip()]
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(auth_router)
app.include_router(user_router)


@app.get("/health", tags=["Health Checks"])
def read_root():
    return {"status": "ok"}
