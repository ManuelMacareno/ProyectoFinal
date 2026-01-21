from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routers.auth import router as auth_router
from app.api.routers.users import router as users_router
from app.api.routers.categories import router as categories_router
from app.api.routers.transactions import router as transactions_router
from app.api.routers.dashboard import router as dashboard_router
from app.db.init_db import init_db

from app import models

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(o) for o in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    @app.on_event("startup")
    def on_startup():
        init_db()

    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(categories_router)
    app.include_router(transactions_router)
    app.include_router(dashboard_router)

    return app

app = create_app()
