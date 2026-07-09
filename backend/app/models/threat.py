from pydantic import BaseModel
from typing import List, Optional


class Threat(BaseModel):
    id: str
    title: str
    source: str
    severity: str
    cve: Optional[str] = None
    affected_products: List[str]
    summary: str
    exploited: bool