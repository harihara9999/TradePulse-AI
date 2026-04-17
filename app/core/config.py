from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Trade Opportunities API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    API_KEY: str = Field(default="dev_secret_key_123", description="API Key for authentication")
    
    # Gemini
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API Key")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
