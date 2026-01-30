from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
# CAMBIA routers → v1.endpoints
from app.api.v1.endpoints import auth, users, categories, transactions, dashboard
from app.db.init_db import init_db

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

    # Incluye desde v1.endpoints
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(categories.router)
    app.include_router(transactions.router)
    app.include_router(dashboard.router)

    return app

app = create_app()