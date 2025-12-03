from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.pelada_resultado import PeladaResultadoCreate, PeladaResultadoRead
from api.controllers.pelada_resultados import list_resultados as list_resultados_ctrl, create_resultado as create_resultado_ctrl
from api.deps import require_auth, security

router = APIRouter(prefix="/pelada-resultados", tags=["pelada-resultados"])

@router.get("/", response_model=List[PeladaResultadoRead])
def list_resultados(db: Session = Depends(get_db)):
    return list_resultados_ctrl(db)

@router.post("/", response_model=PeladaResultadoRead)
def create_resultado(payload: PeladaResultadoCreate, db: Session = Depends(get_db), _credentials: HTTPAuthorizationCredentials = Depends(security), _user = Depends(require_auth)):
    return create_resultado_ctrl(payload, db)
