from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PeladaScoutCreate(BaseModel):
  pelada_id: int
  jogador_id: int
  gols: int
  assistencias: int
  desarmes: int
  defesas_dificeis: int
  faltas: int

class PeladaScoutRead(BaseModel):
  id: int
  pelada_id: int
  jogador_id: int
  gols: int
  assistencias: int
  desarmes: int
  defesas_dificeis: int
  faltas: int
  created_at: datetime
  updated_at: datetime
  model_config = ConfigDict(from_attributes=True)

