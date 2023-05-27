from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    imagga_key: SecretStr
    imagga_secret: SecretStr
    db_host: SecretStr
    db_user: SecretStr
    db_name: SecretStr
    db_pass: SecretStr
    db_port: SecretStr

    class Config:
        env_file = './app/cw.env'
        env_file_encoding = 'utf-8'


config = Settings()
