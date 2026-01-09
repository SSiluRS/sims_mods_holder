import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.config import get_config

app = create_app()
config = get_config()

if __name__ == '__main__':
    PORT = 7066
    HOST = '0.0.0.0'
    
    print(f"🚀 Запуск приложения в режиме: {config.FLASK_ENV}")
    print(f"🗃️  Тип базы данных: {config.DATABASE_TYPE}")
    
    app.run(host=HOST, 
            port=PORT,
            debug=config.DEBUG)