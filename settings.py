from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...

    class Config:
        env_prefix = 'postgres_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


database_settings = DatabaseSettings()
