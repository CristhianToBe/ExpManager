from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.workspace import ValidatePathRequest, ValidatePathResponse, WorkspaceInitRequest, WorkspaceInitResponse, WorkspaceOpenRequest, WorkspaceResponse
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/workspace", tags=["workspace"])
service = WorkspaceService()


@router.post("/init", response_model=WorkspaceInitResponse)
def init_workspace(payload: WorkspaceInitRequest, db: Session = Depends(get_db)):
    workspace, profile, created = service.init_workspace(db, payload.root_path, payload.profile_display_name)
    return WorkspaceInitResponse(workspace=workspace, profile=profile, created_directories=created, db_initialized=True)


@router.post("/open", response_model=WorkspaceResponse)
def open_workspace(payload: WorkspaceOpenRequest, db: Session = Depends(get_db)):
    try:
        return service.open_workspace(db, payload.root_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/current", response_model=WorkspaceResponse | None)
def current_workspace(db: Session = Depends(get_db)):
    return service.current_workspace(db)


@router.post("/validate-path", response_model=ValidatePathResponse)
def validate_path(payload: ValidatePathRequest, db: Session = Depends(get_db)):
    valid, normalized, reason = service.validate_path(db, payload.path)
    return ValidatePathResponse(is_valid=valid, normalized_relative_path=normalized, reason=reason)
