from fastapi import FastAPI
from app.api.router import api_router
from app.api.routes.dashboard import router as dashboard_router
app = FastAPI(
    title="NeoSOC AI API",
    version="1.0.0"
)

app.include_router(api_router)
app.include_router(dashboard_router)
@app.get("/")
def root():
    return {
        "status": "running",
        "application": "NeoSOC AI"
    }