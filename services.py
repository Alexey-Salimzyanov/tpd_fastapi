import httpx
from typing import List, Dict, Any
from config import settings
import logging

logger = logging.getLogger(__name__)

class ExternalAPIService:
    def __init__(self):
        self.api_url = settings.EXTERNAL_API_URL
    
    async def fetch_curriculum_data(self, api_key: str) -> List[Dict[str, Any]]:
        headers = {"X-Apikey": api_key}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.api_url, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Получено {len(data)} записей из API")
                return data
                
        except Exception as e:
            logger.error(f"Ошибка при получении данных: {e}")
            raise
    
    async def get_limited_data(self, api_key: str, limit: int = 20) -> List[Dict[str, Any]]:
        logger.info("Начало получения данных")
        data = await self.fetch_curriculum_data(api_key)
        logger.info(f"Ограничиваем до {limit} записей")
        return data[:limit]