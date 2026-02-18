from fastapi import FastAPI

from app.router.execution_api import router as execution_api
from app.router.read_api import router as read_api
from app.router.proposition_api import router as proposition_api

app = FastAPI(
    title="VendorLogic DIIaC",
    version="1.3.1-phase4",
)

app.include_router(execution_api)
app.include_router(read_api)
app.include_router(proposition_api)
