from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import init_pipeline
from .exceptions import PipelineError, pipeline_error_handler
from .middleware import TimingMiddleware
from .routes import router, system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the heavy AI pipeline on startup
    init_pipeline()
    yield
    # Shutdown events here if necessary


def create_app() -> FastAPI:
    app = FastAPI(
        title="HIRETICA API",
        version="1.0.0",
        description="Deterministic AI-powered candidate ranking engine",
        lifespan=lifespan,
    )

    app.add_middleware(TimingMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(PipelineError, pipeline_error_handler)

    app.include_router(system_router)
    app.include_router(router, prefix="/api/v1")

    return app
