from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    database_user: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str

    class Config:
        env_file = ".env"


settings = DatabaseConfig('webapp/database.env')
