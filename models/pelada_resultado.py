from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.session import Base

class PeladaResultado(Base):
    __tablename__ = "pelada_resultados"
    id = Column(Integer, primary_key=True, index=True)
    pelada_id = Column(Integer, ForeignKey("peladas.id", ondelete="CASCADE"), nullable=False, index=True)
    quantidade_de_jogadores = Column(Integer, default=0, nullable=False)
    total_de_gols = Column(Integer, default=0, nullable=False)
    total_assistencias = Column(Integer, default=0, nullable=False)
    total_desarmes = Column(Integer, default=0, nullable=False)
    total_defesas_dificeis = Column(Integer, default=0, nullable=False)
    total_faltas = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    pelada = relationship("Pelada", back_populates="resultado")

    __table_args__ = (
        UniqueConstraint("pelada_id", name="uq_pelada_resultado_pelada"),
    )
