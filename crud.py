from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from typing import List, Dict, Any
from models import Curriculum
from datetime import datetime
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def upsert_curriculums_bulk(db: Session, raw_data_list: List[Dict[str, Any]]) -> int:
    """Массовый upsert записей"""
    
    prepared_data = []
    for i, raw_data in enumerate(raw_data_list):
        try:
            curriculum_data = prepare_curriculum_data(raw_data)

            prepared_data.append(curriculum_data)
                        
        except Exception as e:
            logger.error(f"Ошибка при подготовке записи {i}: {e}")
            continue
    
    if not prepared_data:
        logger.warning("Нет данных для обработки")
        return 0
    
    try:
        stmt = insert(Curriculum).values(prepared_data)
        
        # Указываем что делать при конфликте (по первичному ключу id)
        update_dict = {
            c.name: c for c in stmt.excluded 
            if c.name not in ['id', 'created']  # Не обновляем id и created
        }
        
        # Добавляем условие ON CONFLICT
        stmt = stmt.on_conflict_do_update(
            index_elements = ['id'],  # Уникальный индекс для проверки конфликта
            set_ = update_dict        # Какие поля обновлять при конфликте
        )
        
        result = db.execute(stmt)
        db.commit()
        
        logger.info(f"Успешно обработано {len(prepared_data)} записей (upsert)")
        return len(prepared_data)
        
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при массовом upsert: {e}", exc_info=True)
        raise

def prepare_curriculum_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        key.lower(): value 
        for key, value in raw_data.items()
    }

