from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.router.execution_router import ExecutionRouter

router = APIRouter()
execution_router = ExecutionRouter()


class ExecutionRequest(BaseModel):
    execution_schema: str
    role: str
    intent: str
    input: Dict[str, Any]
    options: Optional[Dict[str, Any]] = {}


@router.post("/generate")
def generate(req: ExecutionRequest):
    request_dict = req.dict()
    # Normalise back to internal router contract
    request_dict["schema"] = request_dict.pop("execution_schema")

    result = execution_router.route(request_dict)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result)

    return result
