from pydantic_settings import BaseSettings

import os
from dotenv import load_dotenv


load_dotenv()

class Settings_DB(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings_DB()

settings.DB_HOST = os.getenv('DB_HOST')
settings.DB_PORT = os.getenv('DB_PORT')
settings.DB_USER = os.getenv('DB_USER')
settings.DB_PASS = os.getenv('DB_PASS')
settings.DB_NAME = os.getenv('DB_NAME')
