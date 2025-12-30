from fastapi import FastAPI
from backend.api.routes import router
from backend.core.seeds import set_global_seeds
from backend.core.paths import ensure_runtime_dirs

def create_app() -> FastAPI:
    set_global_seeds()
    ensure_runtime_dirs()

    app = FastAPI(
        title="S.P.E.C.T.R.A Backend",
        version="1.0",
    )

    app.include_router(router)
    return app


app = create_app()
