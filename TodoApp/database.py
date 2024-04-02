from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

# SQLALCHEMY_DATABASE_URI = "sqlite:///./todos.db"

DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = "5432"
DB_HOST = 'localhost'
DB_USERNAME = "postgres"

# Using this to encode the special characrters in the password
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

# Postgresql database connection
# 'postgresql://DB_NAME_IN_PGADMIN:DB_PASSWORD!@server:port/DB_NAME
URL_DATABASE = f"postgresql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()