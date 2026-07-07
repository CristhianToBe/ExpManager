from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    workspace_loaded: bool
    db_connected: bool


class DbHealthResponse(BaseModel):
    connected: bool
    db_url: str
