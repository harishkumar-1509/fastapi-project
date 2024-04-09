from fastapi import Depends, Path, HTTPException, APIRouter
from models import Todo
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status
from .auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: bool

@router.get('/todos', status_code = status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, 
                        db: db_dependency):
    return db.query(Todo).filter(Todo.owner_id == user.get('id')).all()

@router.get('/todos/{todo_id}', status_code = status.HTTP_200_OK)
async def get_todo_with_id(user: user_dependency, 
                           db: db_dependency, 
                           todo_id: int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, details = 'User authentication failed')
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code = 400, detail = "Todo not found")

@router.post('/todos', status_code = status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, 
                      db: db_dependency, 
                      todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, details = 'User authentication failed')
    todo = Todo(**todo_request.model_dump(), owner_id = user.get('id'))
    db.add(todo)
    db.commit()

@router.put('/todos/{todo_id}', status_code = status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, 
                      db: db_dependency, 
                      todo_request: TodoRequest, 
                      todo_id: int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, details = 'User authentication failed')
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if todo is None:
        raise HTTPException(status_code = 400, detail = "Todo not found")
    
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.complete = todo_request.complete
    todo.priority = todo_request.priority
    
    db.add(todo)
    db.commit()

@router.delete('/todos/{todo_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, 
                      db: db_dependency, 
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, details = 'User authentication failed')
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if todo is None:
        raise HTTPException(status_code = 400, detail = "Todo not found")
    
    db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).delete()
    db.commit()