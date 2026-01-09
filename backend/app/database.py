import sqlite3
try:
    import pymysql
except ImportError:
    pymysql = None
from backend.config import get_config

config = get_config()

def get_db_connection():
    """Получить соединение с базой данных в зависимости от конфигурации"""
    if config.DATABASE_TYPE == 'sqlite':
        return sqlite3.connect(config.SQLITE_DB)
    elif config.DATABASE_TYPE == 'mysql':
        if pymysql is None:
            raise ImportError("pymysql не установлен. Выполните: pip install pymysql")
        return pymysql.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
            charset='utf8mb4',
            autocommit=True
        )
    else:
        raise ValueError(f"Unsupported database type: {config.DATABASE_TYPE}")

def init_db():
    """Инициализировать базу данных в зависимости от типа"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if config.DATABASE_TYPE == 'sqlite':
        # SQLite специфичные настройки
        cursor.execute('PRAGMA foreign_keys = ON;')
        
        # Таблица тегов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица модов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                image_url TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE,
                download_link TEXT
            )
        ''')
        
        # Таблица связей модов и тегов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mod_tags (
                mod_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                PRIMARY KEY (mod_id, tag_id),
                FOREIGN KEY (mod_id) REFERENCES mods(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        ''')
    else:
        # MySQL специфичные настройки
        # Таблица тегов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Таблица модов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mods (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title TEXT NOT NULL,
                image_url TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE,
                download_link TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Таблица связей модов и тегов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mod_tags (
                mod_id INT NOT NULL,
                tag_id INT NOT NULL,
                PRIMARY KEY (mod_id, tag_id),
                FOREIGN KEY (mod_id) REFERENCES mods(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
    
    conn.commit()
    conn.close()

def get_all_mods():
    """Получить все моды из БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mods ORDER BY id DESC")
    mods = cursor.fetchall()
    conn.close()
    return mods

def add_mod(mod_data):
    """Добавить мод в БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if config.DATABASE_TYPE == 'sqlite':
        cursor.execute('''
            INSERT OR IGNORE INTO mods 
            (title, image_url, link, download_link) 
            VALUES (?, ?, ?, ?)
        ''', (
            mod_data['title'],
            mod_data['image_url'],
            mod_data['link'],
            mod_data.get('download_link', '')
        ))
    else:
        cursor.execute('''
            INSERT IGNORE INTO mods 
            (title, image_url, link, download_link) 
            VALUES (%s, %s, %s, %s)
        ''', (
            mod_data['title'],
            mod_data['image_url'],
            mod_data['link'],
            mod_data.get('download_link', '')
        ))
    
    conn.commit()
    conn.close()

def delete_mod(mod_id):
    """Удалить мод по ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if config.DATABASE_TYPE == 'sqlite':
        cursor.execute("DELETE FROM mods WHERE id = ?", (mod_id,))
    else:
        cursor.execute("DELETE FROM mods WHERE id = %s", (mod_id,))
    
    conn.commit()
    conn.close()

# Функции для работы с тегами (аналогично, с поддержкой обоих типов БД)
def get_all_tags():
    """Получить все теги из БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tags ORDER BY name")
    tags = cursor.fetchall()
    conn.close()
    return tags

def add_tag(tag_name):
    """Добавить тег в БД с проверкой уникальности"""
    if not tag_name or len(tag_name.strip()) < 2:
        raise ValueError("Название тега должно содержать минимум 2 символа")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if config.DATABASE_TYPE == 'sqlite':
            cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag_name.strip(),))
        else:
            cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag_name.strip(),))
        conn.commit()
        return cursor.lastrowid
    except (sqlite3.IntegrityError, pymysql.IntegrityError):
        conn.close()
        raise ValueError(f"Тег '{tag_name}' уже существует")
    finally:
        conn.close()

def update_tag(tag_id, new_name):
    """Обновляет название тега"""
    if not new_name or len(new_name.strip()) < 2:
        raise ValueError("Название тега должно содержать минимум 2 символа")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Для SQLite и MySQL используем разные запросы
        if config.DATABASE_TYPE == 'sqlite':
            # Проверяем, существует ли тег с таким именем (кроме текущего)
            cursor.execute("SELECT id FROM tags WHERE name = ? AND id != ?", (new_name.strip(), tag_id))
            existing = cursor.fetchone()
            if existing:
                conn.close()
                raise ValueError(f"Тег '{new_name}' уже существует")
            
            cursor.execute("UPDATE tags SET name = ? WHERE id = ?", (new_name.strip(), tag_id))
        else:
            # Для MySQL используем INSERT IGNORE с проверкой
            cursor.execute("SELECT id FROM tags WHERE name = %s AND id != %s", (new_name.strip(), tag_id))
            existing = cursor.fetchone()
            if existing:
                conn.close()
                raise ValueError(f"Тег '{new_name}' уже существует")
            
            cursor.execute("UPDATE tags SET name = %s WHERE id = %s", (new_name.strip(), tag_id))
        
        if cursor.rowcount == 0:
            conn.close()
            raise ValueError("Тег не найден")
        conn.commit()
    except Exception as e:
        conn.close()
        raise e
    finally:
        conn.close()

def delete_tag(tag_id):
    """Удалить тег из БД (каскадное удаление из связей)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if config.DATABASE_TYPE == 'sqlite':
        cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    else:
        cursor.execute("DELETE FROM tags WHERE id = %s", (tag_id,))
    
    conn.commit()
    conn.close()

def get_tags_for_mod(mod_id):
    """Получить все теги для конкретного мода"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if config.DATABASE_TYPE == 'sqlite':
        cursor.execute('''
            SELECT t.id, t.name 
            FROM tags t
            JOIN mod_tags mt ON t.id = mt.tag_id
            WHERE mt.mod_id = ?
            ORDER BY t.name
        ''', (mod_id,))
    else:
        cursor.execute('''
            SELECT t.id, t.name 
            FROM tags t
            JOIN mod_tags mt ON t.id = mt.tag_id
            WHERE mt.mod_id = %s
            ORDER BY t.name
        ''', (mod_id,))
    
    tags = cursor.fetchall()
    conn.close()
    return tags

def add_tag_to_mod(mod_id, tag_id):
    """Добавить тег к моду"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if config.DATABASE_TYPE == 'sqlite':
            cursor.execute("INSERT OR IGNORE INTO mod_tags (mod_id, tag_id) VALUES (?, ?)", 
                         (mod_id, tag_id))
        else:
            cursor.execute("INSERT IGNORE INTO mod_tags (mod_id, tag_id) VALUES (%s, %s)", 
                         (mod_id, tag_id))
        conn.commit()
    except Exception as e:
        conn.close()
        raise ValueError(f"Ошибка при добавлении тега к моду: {str(e)}")
    finally:
        conn.close()

def remove_tag_from_mod(mod_id, tag_id):
    """Удалить тег из мода"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if config.DATABASE_TYPE == 'sqlite':
        cursor.execute("DELETE FROM mod_tags WHERE mod_id = ? AND tag_id = ?", 
                      (mod_id, tag_id))
    else:
        cursor.execute("DELETE FROM mod_tags WHERE mod_id = %s AND tag_id = %s", 
                      (mod_id, tag_id))
    
    conn.commit()
    conn.close()