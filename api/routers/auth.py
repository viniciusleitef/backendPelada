from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.auth import LoginRequest, TokenResponse, CurrentUser
from api.controllers.auth import login as login_ctrl, logout as logout_ctrl
from api.deps import require_auth, security
from models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token, _ = login_ctrl(payload, db)
    return TokenResponse(access_token=token)

@router.post("/logout", status_code=204)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    logout_ctrl(token, db)

@router.get("/me", response_model=CurrentUser)
def me(credentials: HTTPAuthorizationCredentials = Depends(security), user: User = Depends(require_auth)):
    return CurrentUser(id=user.id, nome=user.nome, email=user.email, tipo=str(user.tipo))
