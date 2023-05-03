from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    imagga_key: SecretStr
    imagga_secret: SecretStr
    db_host: SecretStr
    db_user: SecretStr
    db_name: SecretStr
    db_pass: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
