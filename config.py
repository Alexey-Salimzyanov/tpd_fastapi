from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TPD"
    DATABASE_URL: str = "postgresql+psycopg2://postgres:OFSHe23jfaF1@localhost:5432/tpd_db"  
    EXTERNAL_API_URL: str = "https://api.ciu.nstu.ru/v1.1/student/get_data/react/curriculum"

settings = Settings()