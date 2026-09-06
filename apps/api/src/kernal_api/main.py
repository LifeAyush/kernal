from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kernal_api.routes.memory import router as memory_router
from kernal_api.routes.workflows import router as workflows_router
from kernal_api.settings import settings
from kernal_core.storage import configure_from_env, init_schema, is_available


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    configure_from_env()
    if is_available():
        init_schema()
    yield


app: FastAPI = FastAPI(title="Kernal", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(memory_router)
app.include_router(workflows_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
