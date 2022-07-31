from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Clinic API"
    
    class Config:
        env_file = ".env"