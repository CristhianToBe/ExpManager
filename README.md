# Gestor de Expedientes

Aplicación desktop local-first para gestión de expedientes. Esta implementación corresponde únicamente a la **Fase 1**: base técnica de monorepo, backend local, shell Electron, pantalla Vue inicial, workspace SQLite y validación básica de rutas.

## Alcance de Fase 1

Incluido:
- Monorepo base.
- Backend local con FastAPI.
- Endpoints `GET /api/v1/health`, `GET /api/v1/health/db`, `POST /api/v1/workspace/init`, `POST /api/v1/workspace/open`, `GET /api/v1/workspace/current` y `POST /api/v1/workspace/validate-path`.
- Modelos mínimos: `Workspace`, `Profile`, `AuditEvent`.
- SQLite local en `.gestor/gestor.db`, `config.json`, `.gestor/logs` y perfil local mínimo.
- Electron con `nodeIntegration: false`, `contextIsolation: true` y preload seguro.
- Vue 3 + TypeScript + Vite + Tailwind + Pinia + TanStack Query.
- Tests mínimos del backend.

No incluido todavía: expedientes, documentos, vencimientos, Scrum/Jira, hoja de trabajo, dashboard real, Gantt, reportes, OCR e instalador final.

## Estructura

```text
apps/
  api/
    app/{core,models,routers,schemas,services}/
    tests/
  desktop/electron/
    main/
    preload/
    renderer/
```

## Instalación

Backend:

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e '.[dev]'
```

Desktop / frontend, desde la raíz:

```bash
npm install
```

## Ejecución

Backend solo:

```bash
cd apps/api
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Frontend solo:

```bash
npm run dev:renderer
```

App completa en modo dev:

```bash
npm run dev:desktop
```

Omitir arranque automático de FastAPI desde Electron:

```bash
GESTOR_SKIP_BACKEND_START=1 npm run dev:desktop
```

## Tests

```bash
cd apps/api
source .venv/bin/activate
pytest
```

## Workspace local

Al inicializar un workspace se crea:

```text
<workspace>/
  .gestor/
    gestor.db
    config.json
    logs/
```

SQLite guarda únicamente metadatos y configuración local mínima. Los binarios documentales se guardarán en filesystem en fases posteriores, nunca en SQLite.

## Seguridad local aplicada en Fase 1

- El renderer de Electron no tiene acceso directo a `fs`, `path`, `shell` ni `child_process`.
- `nodeIntegration` está desactivado.
- `contextIsolation` está activado.
- El preload expone solo `selectWorkspace()`, `getBackendStatus()` y `getAppVersion()`.
- La validación de rutas del backend acepta rutas dentro del workspace y rechaza path traversal o rutas externas.

## Decisiones fijadas para fases futuras

- El día planificado vivirá en `SprintTask.planned_date`; no se usará `Task.planned_date` en el MVP.
- La asociación documento-tarea será many-to-many mediante `DocumentTaskLink`.
- Vue no accederá directamente al filesystem; Electron mediará selección local y FastAPI validará rutas destino dentro del workspace.
