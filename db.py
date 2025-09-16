from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Создаем движок для подключения к PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Создаем фабрику сессий для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()

# Функция-генератор для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        # Возвращаем сессию для использования
        yield db
    finally:
        # Всегда закрываем сессию после использования
        db.close()