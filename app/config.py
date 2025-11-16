from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str
    database_username: str
    SECRET_KEY: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"  # This tells Pydantic to read the .env file

# Create one instance of the settings to be used everywhere
settings = Settings()