"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config import get_settings, print_config, validate_config
from .routes import poi, trip

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validate configuration and print startup information."""
    print("\n" + "=" * 60)
    print(f"Smart Trip Planner v{settings.app_version}")
    print("=" * 60)
    print_config()
    validate_config()
    print(f"\nAPI docs: http://localhost:{settings.port}/docs")
    print("=" * 60 + "\n")
    yield
    print("\nApplication stopped.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Multi-agent trip planner powered by FastAPI, MCP and HelloAgents.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trip.router, prefix="/api")
app.include_router(poi.router, prefix="/api")


@app.get("/")
async def root():
    """Service metadata."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health():
    """Liveness probe."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )