from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate
from core.security import hash_password

def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id.desc()).all()

def create_user(payload: UserCreate, db: Session) -> User:
    item = User(
        nome=payload.nome,
        cpf=payload.cpf,
        telefone=payload.telefone,
        email=payload.email,
        senha_hash=hash_password(payload.senha),
        tipo=payload.tipo,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
