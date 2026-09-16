from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # db_user: str
    # db_password: str
    # db_host: str
    # db_port: str
    # db_name: str
    db_url: str
    debug_mode: bool
    dev_ip: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()