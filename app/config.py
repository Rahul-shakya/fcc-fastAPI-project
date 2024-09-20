from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # pydantic handles tthe env as CASE INSENSITIVE
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str

    # for JSON web token
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'

settings = Settings()
