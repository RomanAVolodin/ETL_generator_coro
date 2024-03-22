from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='postgres_', env_file='.env', env_file_encoding='utf-8')

    dbname: str = Field(..., alias='POSTGRES_DB')
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...


database_settings = DatabaseSettings()
