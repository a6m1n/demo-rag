from fastapi import FastAPI
from fastapi_injector import attach_injector
from injector import Injector

from app.core.injector import CoreModule
from app.ai_engine.routes import ai_router
from app.core.setup_pydiator import setup_pydiator


def setup_injector():
    """Creates root injector module, all modules need to be defined here."""
    injector = Injector(
        [
            CoreModule,
        ]
    )

    return injector


def create_app() -> FastAPI:
    app = FastAPI()

    # API
    app.include_router(ai_router, prefix="/ai-engine", tags=["AI Engine"])

    # DI
    injector = setup_injector()
    attach_injector(app, injector)
    setup_pydiator(injector)

    return app
