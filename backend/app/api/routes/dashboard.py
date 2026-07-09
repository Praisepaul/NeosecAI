from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
async def dashboard():

    return {
        "securityScore":82,
        "criticalAlerts":3,
        "openIncidents":7
    }