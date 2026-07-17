from fastapi import APIRouter

from app.services.dashboard_service import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def dashboard():

    return dashboard_service.get_dashboard()
