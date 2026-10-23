from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_env: str = "local"
    auth_mode: str = "mock"
    database_url: str = "sqlite:///./mplads_sentinel.db"
    audit_log_path: str = "./audit.jsonl"
    max_upload_bytes: int = 2_000_000
    max_ingest_rows: int = 1000
    rate_limit_per_minute: int = 120
    google_cloud_project: str = ""
    google_cloud_location: str = "asia-south1"
    bigquery_dataset: str = "mplads_sentinel"
    vertex_model: str = "gemini-2.5-flash"
    firebase_project_id: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
