from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "todo-list-api"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/todo-list"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
    