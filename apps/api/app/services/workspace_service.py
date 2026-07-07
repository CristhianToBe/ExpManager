import json
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from app.core.config import get_runtime_state_path, get_settings
from app.core.database import SessionLocal, configure_database, create_all
from app.core.paths import relative_to_workspace, resolve_inside_workspace
from app.models import AuditEvent, Profile, Workspace


class WorkspaceService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _technical_paths(self, root: Path) -> tuple[Path, Path, Path, Path]:
        technical_dir = root / self.settings.technical_dir_name
        return technical_dir, technical_dir / self.settings.db_filename, technical_dir / self.settings.workspace_config_name, technical_dir / "logs"

    def _configure_workspace_db(self, db_path: Path) -> None:
        configure_database(f"sqlite:///{db_path.as_posix()}")
        create_all()

    def _write_runtime(self, root: Path, db_path: Path) -> None:
        state_path = get_runtime_state_path()
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps({"workspace_root": str(root), "db_path": str(db_path)}, indent=2), encoding="utf-8")

    def load_runtime_workspace(self) -> bool:
        state_path = get_runtime_state_path()
        if not state_path.exists():
            return False
        data = json.loads(state_path.read_text(encoding="utf-8"))
        db_path = Path(data["db_path"])
        if not db_path.exists():
            return False
        self._configure_workspace_db(db_path)
        return True

    def init_workspace(self, db: Session, root_path: str, profile_display_name: str) -> tuple[Workspace, Profile, list[str]]:
        root = Path(root_path).expanduser().resolve()
        root.mkdir(parents=True, exist_ok=True)
        technical_dir, db_path, config_path, logs_dir = self._technical_paths(root)
        created: list[str] = []
        for directory in (technical_dir, logs_dir):
            if not directory.exists():
                directory.mkdir(parents=True)
                created.append(str(directory))
        self._configure_workspace_db(db_path)
        self._write_runtime(root, db_path)
        db.close()
        db = SessionLocal()
        db.query(Workspace).update({Workspace.is_active: False})
        workspace = Workspace(name=root.name or "Workspace", root_path=str(root), app_version=self.settings.app_version, is_active=True)
        db.add(workspace)
        db.flush()
        initials = "".join(part[0].upper() for part in profile_display_name.split()[:2]) or "UL"
        profile = Profile(display_name=profile_display_name, initials=initials, is_default=True)
        db.add(profile)
        db.flush()
        db.add(AuditEvent(workspace_id=workspace.id, entity_type="workspace", entity_id=str(workspace.id), event_type="workspace.initialized", title="Workspace inicializado", description=f"Workspace creado en {root}", created_by_profile_id=profile.id))
        db.commit()
        db.refresh(workspace)
        db.refresh(profile)
        config = {"workspace_id": workspace.id, "workspace_name": workspace.name, "workspace_root": str(root), "db_path": str(db_path), "app_version": self.settings.app_version, "created_at": datetime.utcnow().isoformat(), "default_profile_id": profile.id}
        config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
        db.expunge(workspace)
        db.expunge(profile)
        db.close()
        return workspace, profile, created

    def open_workspace(self, db: Session, root_path: str) -> Workspace:
        root = Path(root_path).expanduser().resolve()
        _, db_path, config_path, _ = self._technical_paths(root)
        if not db_path.exists() or not config_path.exists():
            raise FileNotFoundError("El workspace no contiene .gestor/gestor.db y config.json")
        self._configure_workspace_db(db_path)
        self._write_runtime(root, db_path)
        db.close()
        db = SessionLocal()
        workspace = db.query(Workspace).filter(Workspace.is_active.is_(True)).order_by(Workspace.id.desc()).first()
        if workspace is None:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            workspace = Workspace(name=config.get("workspace_name", root.name), root_path=str(root), app_version=self.settings.app_version)
            db.add(workspace)
        workspace.last_opened_at = datetime.utcnow()
        db.commit()
        db.refresh(workspace)
        db.expunge(workspace)
        db.close()
        return workspace

    def current_workspace(self, db: Session) -> Workspace | None:
        return db.query(Workspace).filter(Workspace.is_active.is_(True)).order_by(Workspace.id.desc()).first()

    def validate_path(self, db: Session, candidate: str):
        workspace = self.current_workspace(db)
        if workspace is None:
            return False, None, "No hay workspace activo"
        valid, target, reason = resolve_inside_workspace(Path(workspace.root_path), candidate)
        if not valid or target is None:
            return False, None, reason
        return True, relative_to_workspace(Path(workspace.root_path), target), None
