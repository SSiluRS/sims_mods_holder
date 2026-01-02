import os
from dotenv import load_dotenv

# Загружаем .env файл, если он существует
if os.path.exists('.env'):
    load_dotenv()

class Config:
    """Базовая конфигурация"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    
    # Определяем тип базы данных
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')  # 'sqlite' или 'mysql'
    
    # SQLite конфигурация
    SQLITE_DB = os.getenv('SQLITE_DB', 'database.db')
    
    # MySQL конфигурация
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

class DevelopmentConfig(Config):
    """Конфигурация для разработки (локально)"""
    DEBUG = True
    DATABASE_TYPE = 'sqlite'  # Всегда использовать SQLite в разработке

class ProductionConfig(Config):
    """Конфигурация для продакшена (сервер)"""
    DEBUG = False
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'mysql')  # По умолчанию MySQL

# Выбираем конфигурацию в зависимости от окружения
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Получить конфигурацию в зависимости от окружения"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])()