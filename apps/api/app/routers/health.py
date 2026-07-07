from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db, get_engine
from app.schemas.health import DbHealthResponse, HealthResponse
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/health", tags=["health"])


def _workspace_loaded_safely(db: Session) -> bool:
    try:
        return WorkspaceService().current_workspace(db) is not None
    except SQLAlchemyError:
        return False


@router.get("", response_model=HealthResponse)
def health(db: Session = Depends(get_db)):
    db_connected = True
    try:
        db.execute(text("select 1"))
    except SQLAlchemyError:
        db_connected = False
    return HealthResponse(
        status="ok",
        version=get_settings().app_version,
        workspace_loaded=_workspace_loaded_safely(db) if db_connected else False,
        db_connected=db_connected,
    )


@router.get("/db", response_model=DbHealthResponse)
def db_health(db: Session = Depends(get_db)):
    db.execute(text("select 1"))
    return DbHealthResponse(connected=True, db_url=str(get_engine().url))
