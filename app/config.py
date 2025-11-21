"""
Application configuration settings using Pydantic.
"""
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str
    database_username: str
    SECRET_KEY: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        """
        Pydantic configuration.
        """
        env_file = ".env"

# Create one instance of the settings to be used everywhere
settings = Settings()