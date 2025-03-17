from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="enviroments/.env")
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_DB_CACHE: int
    SQLALCHEMY_DATABASE_URL: str
    TEST_DATABASE_URL: str

#экземпляр класса (.атрибут класса)
settings = Settings()
