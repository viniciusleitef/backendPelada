from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.player import PlayerCreate, PlayerRead, PlayerUpdate
from api.controllers.players import list_players as list_players_ctrl, create_player as create_player_ctrl
from api.controllers.players import update_player as update_player_ctrl
from api.deps import require_auth, security

router = APIRouter(prefix="/jogadores", tags=["jogadores"])

@router.get("/", response_model=List[PlayerRead])
def list_players(db: Session = Depends(get_db)):
    return list_players_ctrl(db)

@router.post("/", response_model=PlayerRead)
def create_player(payload: PlayerCreate, db: Session = Depends(get_db), _credentials: HTTPAuthorizationCredentials = Depends(security), _user = Depends(require_auth)):
    return create_player_ctrl(payload, db)

@router.put("/{player_id}", response_model=PlayerRead)
def update_player(player_id: int, payload: PlayerUpdate, db: Session = Depends(get_db), _credentials: HTTPAuthorizationCredentials = Depends(security), _user = Depends(require_auth)):
    return update_player_ctrl(player_id, payload, db)
