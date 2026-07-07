from pydantic import BaseModel, Field


class WorkspaceInitRequest(BaseModel):
    root_path: str
    profile_display_name: str = "Usuario Local"


class WorkspaceOpenRequest(BaseModel):
    root_path: str


class WorkspaceResponse(BaseModel):
    id: int
    name: str
    root_path: str
    technical_dir_relative_path: str
    db_relative_path: str
    config_relative_path: str
    app_version: str
    is_active: bool
    model_config = {"from_attributes": True}


class ProfileResponse(BaseModel):
    id: int
    display_name: str
    initials: str
    role: str
    is_default: bool
    model_config = {"from_attributes": True}


class WorkspaceInitResponse(BaseModel):
    workspace: WorkspaceResponse
    profile: ProfileResponse
    created_directories: list[str]
    db_initialized: bool


class ValidatePathRequest(BaseModel):
    path: str = Field(..., min_length=1)


class ValidatePathResponse(BaseModel):
    is_valid: bool
    normalized_relative_path: str | None = None
    reason: str | None = None
