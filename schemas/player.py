from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class PlayerCreate(BaseModel):
  nome: str = Field(min_length=1)
  total_gols: int = 0
  total_assistencias: int = 0
  total_desarmes: int = 0
  total_defesas_dificeis: int = 0
  total_faltas: int = 0
  total_partidas: int = 0

class PlayerUpdate(BaseModel):
  nome: str = Field(min_length=1)
  total_gols: int
  total_assistencias: int
  total_desarmes: int
  total_defesas_dificeis: int
  total_faltas: int
  total_partidas: int

class PlayerRead(BaseModel):
  id: int
  nome: str
  total_gols: int
  total_assistencias: int
  total_desarmes: int
  total_defesas_dificeis: int
  total_faltas: int
  total_partidas: int
  created_at: datetime
  updated_at: datetime
  model_config = ConfigDict(from_attributes=True)
