from fastapi import FastAPI
import models
from models import *
from database import engine
from routers import auth, todos, admin

app = FastAPI()

# This line will create all the tables and columns in the database
models.Base.metadata.create_all(bind = engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)

