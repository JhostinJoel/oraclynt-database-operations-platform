from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "TEST"
    read_only: bool = True
    production_writes: bool = False
    arbitrary_sql: bool = False
    arbitrary_plsql: bool = False
    kill_switch: bool = False
    max_rows: int = 1000
    command_timeout_seconds: int = 5
    oracle_host: str | None = None
    oracle_port: int = 1521
    oracle_service: str | None = None
    oracle_user: str | None = None
    oracle_password: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
