import os
from dotenv import load_dotenv

load_dotenv()

DB_PREFIX = "mysql+pymysql"
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"{DB_PREFIX}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"