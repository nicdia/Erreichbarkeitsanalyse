from dotenv import load_dotenv
import os
import sqlalchemy

def get_env():
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")
    return (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


def connect2DB():
    params = get_env()
    engine = sqlalchemy.create_engine(f"postgresql://{params[0]}:{params[1]}@{params[2]}:{params[3]}/{params[4]}")
    return engine