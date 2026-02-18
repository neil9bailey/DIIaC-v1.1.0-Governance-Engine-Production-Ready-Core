from fastapi import APIRouter, Depends

from app.api.rbac import require_roles
from app.services.ledger import read_ledger, verify_ledger


router = APIRouter()


@router.get(
    "/api/read/audit",
    dependencies=[Depends(require_roles(["AUDITOR", "EXECUTOR"]))],
)
def read_audit():
    return read_ledger()


@router.get(
    "/api/read/verify-ledger",
    dependencies=[Depends(require_roles(["AUDITOR", "EXECUTOR"]))],
)
def verify():
    return verify_ledger()
