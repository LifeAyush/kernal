from fastapi import APIRouter, Depends, HTTPException

from kernal_api.deps import require_cron_secret, require_storage

router: APIRouter = APIRouter(
    prefix="/api/workflows",
    dependencies=[Depends(require_storage), Depends(require_cron_secret)],
)


@router.post("/linkedin.find_people/run")
def trigger_find_people() -> None:
    raise HTTPException(status_code=501, detail="linkedin.find_people is not implemented")
