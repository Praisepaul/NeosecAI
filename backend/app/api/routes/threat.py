from fastapi import APIRouter, HTTPException

from app.services.threat_service import threat_service

router = APIRouter(
    prefix="/threats",
    tags=["Threat Intelligence"],
)


@router.get("/")
def get_threat_summaries():
    return threat_service.get_all()


@router.get("/{cve}")
def get_threat_by_cve(cve: str):

    threat = threat_service.get_by_cve(cve)

    if not threat:
        raise HTTPException(
            status_code=404,
            detail=f"Threat {cve} not found",
        )

    return threat


@router.post("/sync")
def sync_threats():
    return threat_service.sync()
