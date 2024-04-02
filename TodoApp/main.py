from fastapi import FastAPI, Depends, Path, HTTPException
import models
from models import *
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

# This line will create all the tables and columns in the database
models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: bool

@app.get('/todos', status_code = status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    return db.query(Todo).all()

@app.get('/todos/{todo_id}', status_code = status.HTTP_200_OK)
async def get_todo_with_id(db: db_dependency, todo_id: int = Path(gt = 0)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code = 400, detail = "Todo not found")

@app.post('/todos', status_code = status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo = Todo(**todo_request.model_dump())
    db.add(todo)
    db.commit()

@app.put('/todos/{todo_id}', status_code = status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt = 0)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code = 400, detail = "Todo not found")
    
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.complete = todo_request.complete
    todo.priority = todo_request.priority
    
    db.add(todo)
    db.commit()

@app.delete('/todos/{todo_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code = 400, detail = "Todo not found")
    
    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()