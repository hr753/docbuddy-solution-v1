from fastapi import APIRouter

from app.deps import SettingsDep, StoreDep
from app.schemas import HealthOut

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthOut)
async def health(settings: SettingsDep, store: StoreDep) -> HealthOut:
    """Public: load balancers and uptime checkers call this without a key."""
    return HealthOut(status="ok", version=settings.version, documents=store.count())
