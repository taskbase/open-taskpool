from pydantic import BaseSettings


class Settings(BaseSettings):
    taskpool_db_path: str = "taskpool.db"


settings = Settings()
