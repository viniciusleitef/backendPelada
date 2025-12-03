from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.session import Base

class PeladaScout(Base):
    __tablename__ = "pelada_scouts"
    id = Column(Integer, primary_key=True, index=True)
    pelada_id = Column(Integer, ForeignKey("peladas.id", ondelete="CASCADE"), nullable=False, index=True)
    jogador_id = Column(Integer, ForeignKey("jogadores.id", ondelete="CASCADE"), nullable=False, index=True)
    gols = Column(Integer, default=0, nullable=False)
    assistencias = Column(Integer, default=0, nullable=False)
    desarmes = Column(Integer, default=0, nullable=False)
    defesas_dificeis = Column(Integer, default=0, nullable=False)
    faltas = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    pelada = relationship("Pelada", back_populates="scouts")
    jogador = relationship("Player", back_populates="scouts")

    __table_args__ = (
        UniqueConstraint("pelada_id", "jogador_id", name="uq_pelada_jogador"),
    )

