from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=schemas.DashboardSummary)
def get_summary(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    return crud.get_dashboard_summary(db=db, usuario_id=current_user.id)
