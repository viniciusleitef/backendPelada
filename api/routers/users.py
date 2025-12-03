from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.user import UserCreate, UserRead
from api.controllers.users import list_users as list_users_ctrl, create_user as create_user_ctrl

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

# @router.get("/", response_model=List[UserRead])
# def list_users(db: Session = Depends(get_db)):
#     return list_users_ctrl(db)

# @router.post("/", response_model=UserRead)
# def create_user(payload: UserCreate, db: Session = Depends(get_db)):
#     return create_user_ctrl(payload, db)
