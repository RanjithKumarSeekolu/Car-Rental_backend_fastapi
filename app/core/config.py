from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env", extra="ignore")

  firebase_service_account_json: str = ""
  firebase_credentials_path: str = "firebase-admin-sdk.json"
  firebase_storage_bucket: str = ""
  cors_origin: str = ""

settings = Settings()