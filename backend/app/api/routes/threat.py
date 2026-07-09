from fastapi import APIRouter
from app.services.threat_service import threat_service

router = APIRouter(
    prefix="/threats",
    tags=["Threat Intelligence"],
)


@router.get("/")
def get_all():

    return threat_service.get_all()