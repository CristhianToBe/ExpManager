from pathlib import Path


def resolve_inside_workspace(workspace_root: Path, candidate: str | Path) -> tuple[bool, Path | None, str | None]:
    root = workspace_root.expanduser().resolve()
    raw = Path(candidate)
    try:
        target = raw.expanduser().resolve() if raw.is_absolute() else (root / raw).resolve()
    except (OSError, RuntimeError) as exc:
        return False, None, f"No se pudo resolver la ruta: {exc}"
    try:
        target.relative_to(root)
    except ValueError:
        return False, None, "La ruta está fuera del workspace autorizado"
    return True, target, None


def relative_to_workspace(workspace_root: Path, candidate: Path) -> str:
    return candidate.resolve().relative_to(workspace_root.resolve()).as_posix()
