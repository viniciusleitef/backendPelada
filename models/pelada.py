from sqlalchemy import Column, Integer, String, Date, Boolean, Text, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.session import Base

class Pelada(Base):
    __tablename__ = "peladas"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    horario = Column(String(30), nullable=False)
    local = Column(String(200), nullable=False)
    teve_arbitro = Column(Boolean, default=False, nullable=False)
    comentarios = Column(Text, nullable=True)
    custo_do_campo = Column(Numeric(10, 2), default=0, nullable=False)
    custo_do_arbitro = Column(Numeric(10, 2), default=0, nullable=False)
    custo_adicional = Column(Numeric(10, 2), default=0, nullable=False)
    custo_total = Column(Numeric(10, 2), default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    scouts = relationship("PeladaScout", back_populates="pelada", cascade="all, delete-orphan")
    resultado = relationship("PeladaResultado", back_populates="pelada", uselist=False, cascade="all, delete-orphan")
