from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.pelada import PeladaCreate, PeladaRead, PeladaUpdate
from api.controllers.peladas import (
    list_peladas as list_peladas_ctrl,
    create_pelada as create_pelada_ctrl,
    delete_pelada as delete_pelada_ctrl,
    update_pelada as update_pelada_ctrl,
)
from api.deps import require_auth, security

router = APIRouter(prefix="/peladas", tags=["peladas"])

@router.get("/", response_model=List[PeladaRead])
def list_peladas(db: Session = Depends(get_db)):
    return list_peladas_ctrl(db)

@router.post("/", response_model=PeladaRead)
def create_pelada(payload: PeladaCreate, db: Session = Depends(get_db), _credentials: HTTPAuthorizationCredentials = Depends(security), _user = Depends(require_auth)):
    return create_pelada_ctrl(payload, db)

@router.delete("/{pelada_id}", status_code=204)
def delete_pelada(pelada_id: int, db: Session = Depends(get_db), _credentials: HTTPAuthorizationCredentials = Depends(security), _user = Depends(require_auth)):
    delete_pelada_ctrl(pelada_id, db)

@router.put("/{pelada_id}", response_model=PeladaRead)
def update_pelada(pelada_id: int, payload: PeladaUpdate, db: Session = Depends(get_db), _credentials: HTTPAuthorizationCredentials = Depends(security), _user = Depends(require_auth)):
    return update_pelada_ctrl(pelada_id, payload, db)
