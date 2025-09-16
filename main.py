# from fastapi import FastAPI, Header
# import uvicorn
# import httpx

# app = FastAPI()
    
# @app.get("/data")
# async def get_data(
#     x_apikey: str = Header(..., alias="X-Apikey")
# ):
#     url = "https://api.ciu.nstu.ru/v1.1/student/get_data/react/curriculum"
    
#     headers = {
#         "X-Apikey": x_apikey
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
        
#         return response.json()[:20]

# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
from fastapi import FastAPI, Header, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from typing import List, Dict, Any
import logging

from config import settings
from db import engine, Base, get_db
from models import Curriculum
from services import ExternalAPIService
from crud import upsert_curriculums_bulk

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup_event():
    """Создает таблицы при запуске приложения"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Таблицы базы данных созданы/проверены")
    except Exception as e:
        logger.error(f"❌ Ошибка создания таблиц: {e}")
        raise

@app.get("/")
async def root():
    return {"message": "Curriculum API Service"}

@app.get("/curriculums")
async def get_and_store_curriculums(
    x_apikey: str = Header(..., alias="X-Apikey"),
    db: Session = Depends(get_db)
):
    try:
        logger.info("🔄 Начало получения данных из внешнего API")
        
        api_service = ExternalAPIService()
        raw_data = await api_service.fetch_curriculum_data(x_apikey)
        
        logger.info(f"✅ Получено {len(raw_data)} записей из API")
        
        # Используем upsert вместо простой вставки
        records_processed = upsert_curriculums_bulk(db, raw_data)
        # Если bulk не работает, используйте ручной вариант:
        # records_processed = upsert_curriculums_manual(db, raw_data)
        
        return {
            "message": "Data processed successfully",
            "operation": "upsert",  # Теперь это upsert, а не insert
            "records_processed": records_processed,
            "total_received": len(raw_data)
        }
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)