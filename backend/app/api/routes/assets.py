from fastapi import APIRouter

from app.assets.asset_service import asset_service

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.post("/seed")
def seed():

    total = asset_service.seed()

    return {"status": "SUCCESS", "assets": total}
