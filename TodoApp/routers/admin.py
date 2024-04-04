from fastapi import Depends, Path, HTTPException, APIRouter
from models import Todo
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/todo', status_code=status.HTTP_200_OK)
async def get_todos(user: user_dependency,
                    db: db_dependency
                    ):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todo).all()