from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PeladaResultadoCreate(BaseModel):
  pelada_id: int
  quantidade_de_jogadores: int
  total_de_gols: int
  total_assistencias: int
  total_desarmes: int
  total_defesas_dificeis: int
  total_faltas: int

class PeladaResultadoRead(BaseModel):
  id: int
  pelada_id: int
  quantidade_de_jogadores: int
  total_de_gols: int
  total_assistencias: int
  total_desarmes: int
  total_defesas_dificeis: int
  total_faltas: int
  created_at: datetime
  updated_at: datetime
  model_config = ConfigDict(from_attributes=True)

