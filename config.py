import os
from dotenv import load_dotenv

# Загружаем .env файл, если он существует
if os.path.exists('.env'):
    load_dotenv()

class Config:
    """Базовая конфигурация"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    # Определяем тип базы данных
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')  # 'sqlite' или 'mysql'
    
    # SQLite конфигурация
    SQLITE_DB = os.getenv('SQLITE_DB', 'sims_mods.db')
    print(f"Using SQLite database file: {SQLITE_DB}")
    
    # MySQL конфигурация
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

def get_config():
    """Получить конфигурацию"""
    return Config()