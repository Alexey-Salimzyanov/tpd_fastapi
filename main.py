from fastapi import FastAPI, Header, Depends, HTTPException
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import httpx
from typing import List, Dict, Any
import logging

from config import settings
from db import engine, Base, get_db
from models import Curriculum
from services import ExternalAPIService
from crud import upsert_curriculums_bulk

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

# Конфигурация из переменных окружения
API_KEY = os.getenv("EXTERNAL_API_KEY")
SYNC_INTERVAL = int(os.getenv("SYNC_INTERVAL_SECONDS", 3600))

@app.on_event("startup")
async def startup_event():
    """Создает таблицы при запуске приложения"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Таблицы базы данных созданы/проверены")
    except Exception as e:
        logger.error(f"Ошибка создания таблиц: {e}")
        raise

@app.on_event("startup")
@repeat_every(seconds=SYNC_INTERVAL)
async def periodic_curriculum_sync():
    """Периодическая синхронизация учебных планов"""      
    if not API_KEY:
        logger.error("API ключ не найден.")
        return
    
    try:
        logger.info("Запуск периодической синхронизации учебных планов")
        
        db = next(get_db())
        try:
            api_service = ExternalAPIService()
            raw_data = await api_service.fetch_curriculum_data(API_KEY)
            
            logger.info(f"Получено {len(raw_data)} записей из API")
            
            records_processed = upsert_curriculums_bulk(db, raw_data)
            
            logger.info(f"Синхронизация завершена. Обработано записей: {records_processed}")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Ошибка при периодической синхронизации: {e}", exc_info=True)


@app.get("/")
async def root():
    return {"message": "Curriculum API Service"}

@app.get("/curriculums")
async def get_and_store_curriculums(
    x_apikey: str = Header(..., alias="X-Apikey"),
    db: Session = Depends(get_db)
):
    try:
        logger.info("Начало получения данных из внешнего API")
        
        api_service = ExternalAPIService()
        raw_data = await api_service.fetch_curriculum_data(x_apikey)
        
        logger.info(f"Получено {len(raw_data)} записей из API")
        
        records_processed = upsert_curriculums_bulk(db, raw_data)
        
        return {
            "message": "Data processed successfully",
            "operation": "upsert",
            "records_processed": records_processed,
            "total_received": len(raw_data)
        }
        
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)