from sqlalchemy.exc import IntegrityError
from db.session import SessionLocal
from models.user import User
from core.security import hash_password

NOME = "Suderley Filho"
CPF = "00000000000"
TELEFONE = "11999999999"
EMAIL = "admin@pelada.sicks"
TIPO = "admin"
SENHA = "flamengotetra"

def main():
    db = SessionLocal()
    try:
        user = User(
            nome=NOME,
            cpf=CPF,
            telefone=TELEFONE,
            email=EMAIL,
            tipo=TIPO,
            senha_hash=hash_password(SENHA),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"OK:{user.id}")
    except IntegrityError:
        db.rollback()
        print("ERROR: usuário já existe")
        raise SystemExit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()

