import os
from dotenv import load_dotenv

load_dotenv(".env")

#DATABASE

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


SQL_ACLCHEMY_KEY = os.getenv("SQL_ACLCHEMY_KEY")