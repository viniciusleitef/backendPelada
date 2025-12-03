from pydantic import BaseModel

class InicioResumo(BaseModel):
  total_peladas: int
  jogadores_ativos: int
  total_gols: int

