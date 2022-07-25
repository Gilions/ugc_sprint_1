from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # ClickHouse
    CH_HOST: str = Field('localhost', env='CH_HOST')
    CH_PORT: int = Field(9000, env='CH_PORT')

    class Config:
        env_file = '.env'


conf = Settings()
