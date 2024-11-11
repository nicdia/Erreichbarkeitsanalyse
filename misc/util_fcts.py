from dotenv import load_dotenv
import os
import sqlalchemy
import json
import logging

def get_env():
    """
    Loads environment variables from .env file and returns a tuple of the DB
    parameters, i.e. (user, password, host, port, name)
    """
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")
    return (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


def connect2DB():
    """
    Establishes a connection to the PostgreSQL database using the
    environment variables set in the .env file.

    Returns:
        sqlalchemy.engine.Engine: A connection engine to the database
    """
    params = get_env()
    engine = sqlalchemy.create_engine(f"postgresql://{params[0]}:{params[1]}@{params[2]}:{params[3]}/{params[4]}")
    return engine

def get_config():
    """
    Loads and returns the configuration settings from a JSON file.

    Returns:
        dict: A dictionary containing the configuration settings.
    """
    with open("config.json", "r") as file:
        config = json.load(file)
    
    return config

def get_logging():
    """
    Configures and returns a logger instance that logs any errors to a file named
    'query_errors.log' in the current working directory.

    Returns:
        logging.Logger: A logger instance that logs errors to a file.
    """

    logging.basicConfig(filename='query_errors.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    return logger


def setup(config_path):
    db_con = connect2DB()
    with open(config_path, "r") as file:
        config = json.load(file)

    return db_con, config