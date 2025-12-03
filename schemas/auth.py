from pydantic import BaseModel

class LoginRequest(BaseModel):
  email: str
  senha: str

class TokenResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"

class CurrentUser(BaseModel):
  id: int
  nome: str
  email: str
  tipo: str

