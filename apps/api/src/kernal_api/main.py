from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kernal_api.settings import settings

app: FastAPI = FastAPI(title="Kernal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
