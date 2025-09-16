from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from typing import List, Dict, Any
from models import Curriculum
from datetime import datetime
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def upsert_curriculums_bulk(db: Session, raw_data_list: List[Dict[str, Any]]) -> int:
    """Массовый upsert (обновление или вставка) записей"""
    
    prepared_data = []
    
    for i, raw_data in enumerate(raw_data_list):
        try:
            curriculum_data = prepare_curriculum_data(raw_data)
            prepared_data.append(curriculum_data)
            
            if i % 100 == 0:
                logger.info(f"🔄 Подготовлено {i} записей")
                
        except Exception as e:
            logger.error(f"❌ Ошибка при подготовке записи {i}: {e}")
            continue
    
    if not prepared_data:
        logger.warning("⚠️ Нет данных для обработки")
        return 0
    
    try:
        # Создаем statement для upsert
        stmt = insert(Curriculum).values(prepared_data)
        
        # Указываем что делать при конфликте (по первичному ключу id)
        update_dict = {
            c.name: c for c in stmt.excluded 
            if c.name not in ['id', 'created']  # Не обновляем id и created
        }
        
        # Добавляем условие ON CONFLICT
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],  # Уникальный индекс для проверки конфликта
            set_=update_dict        # Какие поля обновлять при конфликте
        )
        
        # Выполняем upsert
        result = db.execute(stmt)
        db.commit()
        
        logger.info(f"✅ Успешно обработано {len(prepared_data)} записей (upsert)")
        return len(prepared_data)
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Ошибка при массовом upsert: {e}", exc_info=True)
        raise

def prepare_curriculum_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Подготавливает данные для создания Curriculum"""
    return {
        'id': raw_data['ID'],
        'id_okso': raw_data.get('ID_OKSO'),
        'id_plan_type': raw_data['ID_PLAN_TYPE'],
        'id_disc_cycle': raw_data.get('ID_DISC_CYCLE'),
        'id_training_forms': raw_data['ID_TRAINING_FORMS'],
        'id_study_period': raw_data['ID_STUDY_PERIOD'],
        'base_credits': raw_data.get('BASE_CREDITS'),
        'var_credits': raw_data.get('VAR_CREDITS'),
        'id_curr_constrs': raw_data.get('ID_CURR_CONSTRS'),
        'id_indep_work_norms': raw_data.get('ID_INDEP_WORK_NORMS'),
        'total_credits': raw_data.get('TOTAL_CREDITS'),
        'is_bach_req': bool(raw_data.get('IS_BACH_REQ', 0)),
        'is_short': bool(raw_data.get('IS_SHORT', 0)),
        'id_stage_req': raw_data.get('ID_STAGE_REQ'),
        'year_enrol': raw_data['YEAR_ENROL'],
        'id_parent_curriculum': raw_data.get('ID_PARENT_CURRICULUM'),
        'copy_number': raw_data.get('COPY_NUMBER', 0),
        'version_number': raw_data.get('VERSION_NUMBER', 0),
        'id_copy_reason': raw_data.get('ID_COPY_REASON'),
        'id_developer': raw_data['ID_DEVELOPER'],
        'id_responsible': raw_data['ID_RESPONSIBLE'],
        'c2h': raw_data['C2H'],
        'c2h_min': raw_data['C2H_MIN'],
        'c2h_max': raw_data['C2H_MAX'],
        'last_modified': parse_datetime(raw_data['LAST_MODIFIED']),
        'created': parse_datetime(raw_data.get('CREATED')),
        'remark': raw_data.get('REMARK'),
        'has_ge': bool(raw_data.get('HAS_GE', 0)),
        'id_status': raw_data['ID_STATUS'],
        'is_by_cycles_bad': bool(raw_data.get('IS_BY_CYCLES_BAD', 0)),
        'credits': raw_data['CREDITS'],
        'publish_date': parse_datetime(raw_data['PUBLISH_DATE']),
        'fsk_facultet': str(raw_data['FSK_FACULTET']) if raw_data.get('FSK_FACULTET') is not None else None,
        'id_dean': raw_data.get('ID_DEAN'),
        'id_chair_head': raw_data.get('ID_CHAIR_HEAD'),
        'id_okso_module': raw_data.get('ID_OKSO_MODULE'),
        'id_okso_profile': raw_data.get('ID_OKSO_PROFILE'),
        'sem_start_profile': raw_data.get('SEM_START_PROFILE'),
        'id_chair': raw_data.get('ID_CHAIR'),
        'type_bac': raw_data.get('TYPE_BAC'),
        'id_level': raw_data.get('ID_LEVEL'),
        'duration_months': raw_data['DURATION_MONTHS'],
        'fk_project_organization': raw_data.get('FK_PROJECT_ORGANIZATION'),
        'id_curriculum_protocol': raw_data.get('ID_CURRICULUM_PROTOCOL'),
        'id_wp_resp': raw_data.get('ID_WP_RESP'),
        'pages': raw_data.get('PAGES'),
        'id_fgos': raw_data.get('ID_FGOS'),
        'fk_foreign_langs': raw_data.get('FK_FOREIGN_LANGS', 0),
        'is_tracks': bool(raw_data.get('IS_TRACKS', 0)),
        'edit_cm_developers': bool(raw_data.get('EDIT_CM_DEVELOPERS', 0)),
        'id_pdf_doc': raw_data.get('ID_PDF_DOC'),
        'id_file_g': raw_data.get('ID_FILE_G')
    }

def parse_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    """Парсит строку datetime с обработкой None"""
    if not datetime_str:
        return None
    try:
        return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        logger.warning(f"⚠️ Не удалось распарсить datetime: {datetime_str}")
        return None