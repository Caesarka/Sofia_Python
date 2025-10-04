from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = 'SECRET_KEY'
    ALGORITHM: str = 'ALGORITHM'
    ACCESS_TOKEN_EXPIRE: min = 1440
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()