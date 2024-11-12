from pydantic import BaseModel

class Settings(BaseModel):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ISIS Mobile"
    DATABASE_URL: str = "sqlite:///./isis_mobile.db"

settings = Settings() 