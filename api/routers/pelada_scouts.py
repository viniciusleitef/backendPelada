from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.pelada_scout import PeladaScoutCreate, PeladaScoutRead
from api.controllers.pelada_scouts import (
    list_scouts as list_scouts_ctrl,
    create_scout as create_scout_ctrl,
    list_scouts_by_pelada as list_scouts_by_pelada_ctrl,
)
from api.deps import require_auth, security

router = APIRouter(prefix="/pelada-scouts", tags=["pelada-scouts"])

@router.get("/", response_model=List[PeladaScoutRead])
def list_scouts(db: Session = Depends(get_db)):
    return list_scouts_ctrl(db)

@router.post("/", response_model=PeladaScoutRead)
def create_scout(payload: PeladaScoutCreate, db: Session = Depends(get_db), _credentials: HTTPAuthorizationCredentials = Depends(security), _user = Depends(require_auth)):
    return create_scout_ctrl(payload, db)

@router.get("/by-pelada/{pelada_id}", response_model=List[PeladaScoutRead])
def list_by_pelada(pelada_id: int, db: Session = Depends(get_db)):
    return list_scouts_by_pelada_ctrl(pelada_id, db)
