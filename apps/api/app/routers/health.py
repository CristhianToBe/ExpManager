from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db, get_engine
from app.schemas.health import DbHealthResponse, HealthResponse
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health(db: Session = Depends(get_db)):
    db_connected = True
    try:
        db.execute(text("select 1"))
    except Exception:
        db_connected = False
    return HealthResponse(status="ok", version=get_settings().app_version, workspace_loaded=WorkspaceService().current_workspace(db) is not None, db_connected=db_connected)


@router.get("/db", response_model=DbHealthResponse)
def db_health(db: Session = Depends(get_db)):
    db.execute(text("select 1"))
    return DbHealthResponse(connected=True, db_url=str(get_engine().url))
