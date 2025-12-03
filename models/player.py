from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.session import Base

class Player(Base):
    __tablename__ = "jogadores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False, unique=True, index=True)
    total_gols = Column(Integer, default=0, nullable=False)
    total_assistencias = Column(Integer, default=0, nullable=False)
    total_desarmes = Column(Integer, default=0, nullable=False)
    total_defesas_dificeis = Column(Integer, default=0, nullable=False)
    total_faltas = Column(Integer, default=0, nullable=False)
    total_partidas = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    scouts = relationship("PeladaScout", back_populates="jogador")
    __table_args__ = (
        UniqueConstraint("nome", name="uq_jogador_nome"),
    )
