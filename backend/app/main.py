from fastapi import FastAPI
from app.api.router import api_router
from app.api.routes.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NeoSOC AI API", version="1.0.0")

app.include_router(api_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"status": "running", "application": "NeoSOC AI"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
