from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.inicio import InicioResumo
from api.controllers.inicio import get_inicio_resumo as get_inicio_resumo_ctrl

router = APIRouter(prefix="/inicio", tags=["inicio"])

@router.get("/", response_model=InicioResumo)
def inicio_resumo(db: Session = Depends(get_db)):
    return get_inicio_resumo_ctrl(db)

