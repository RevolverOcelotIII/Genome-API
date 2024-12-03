from dotenv import load_dotenv
import os

# Carregar o .env
load_dotenv()

# Variáveis globais
ROOT_PATH = os.getenv("ROOT_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA")