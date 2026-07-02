from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import create_all
from app.routers import health, workspace
from app.services.workspace_service import WorkspaceService

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
def startup() -> None:
    WorkspaceService().load_runtime_workspace()
    create_all()


app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(workspace.router, prefix=settings.api_prefix)
