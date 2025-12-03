from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from models.user import User
from models.session import Session as SessionModel
from core.security import verify_password, generate_token, token_expiry
from schemas.auth import LoginRequest, CurrentUser

def login(payload: LoginRequest, db: Session) -> tuple[str, CurrentUser]:
    user = db.query(User).filter(User.email.ilike(payload.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    if not verify_password(payload.senha, user.senha_hash or ""):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = generate_token()
    session = SessionModel(user_id=user.id, token=token, expires_at=token_expiry())
    db.add(session)
    db.commit()
    cu = CurrentUser(id=user.id, nome=user.nome, email=user.email, tipo=str(user.tipo))
    return token, cu

def logout(token: str, db: Session) -> None:
    sess = db.query(SessionModel).filter(SessionModel.token == token).first()
    if sess:
        db.delete(sess)
        db.commit()

