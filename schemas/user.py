from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
  nome: str
  cpf: str
  telefone: str
  email: str
  tipo: str
  senha: str

class UserRead(BaseModel):
  id: int
  nome: str
  cpf: str
  telefone: str
  email: str
  tipo: str
  created_at: datetime
  updated_at: datetime
  model_config = ConfigDict(from_attributes=True)
