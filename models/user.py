from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func

from db.session import Base

UserType = Enum("admin", "comum", name="user_type")

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    senha_hash = Column(String(128), nullable=False)
    tipo = Column(UserType, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
