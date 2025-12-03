from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict

class PeladaJogadorInput(BaseModel):
  jogador_id: int
  gols: int = 0
  assistencias: int = 0
  desarmes: int = 0
  defesas_dificeis: int = 0
  faltas: int = 0

class PeladaCreate(BaseModel):
  data: date
  horario_inicio: time | None = None
  horario_fim: time | None = None
  local: str
  teve_arbitro: bool
  comentarios: str | None = None
  custo_do_campo: float = 0
  custo_do_arbitro: float = 0
  custo_adicional: float = 0
  jogadores: list[PeladaJogadorInput] = []

class PeladaRead(BaseModel):
  id: int
  data: date
  horario: time | str
  local: str
  teve_arbitro: bool
  comentarios: str | None
  custo_do_campo: float
  custo_do_arbitro: float
  custo_adicional: float
  custo_total: float
  created_at: datetime
  updated_at: datetime
  model_config = ConfigDict(from_attributes=True)

class PeladaUpdate(BaseModel):
  data: date
  horario_inicio: time | None = None
  horario_fim: time | None = None
  local: str
  teve_arbitro: bool
  comentarios: str | None = None
  custo_do_campo: float = 0
  custo_do_arbitro: float = 0
  custo_adicional: float = 0
  jogadores: list[PeladaJogadorInput] = []

