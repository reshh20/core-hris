
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import OrgChartNode
from app.services import organization_service

router = APIRouter(prefix="/api/org-chart", tags=["Organization Chart"])


@router.get(
    "",
    response_model=list[OrgChartNode],
    summary="Get organization chart",
    description="Retrieve the full organizational hierarchy as a nested tree structure.",
)
def get_org_chart(db: Session = Depends(get_db)):
    return organization_service.get_org_chart(db)
