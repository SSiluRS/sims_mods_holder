from flask import Flask, render_template, request, redirect, flash, url_for
from database import init_db, get_all_mods, add_mod, delete_mod, get_all_tags, add_tag, update_tag, delete_tag, get_tags_for_mod, add_tag_to_mod, remove_tag_from_mod, get_db_connection
from parser import parse_mod_data
from config import get_config
from flask import jsonify

config = get_config()

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.debug = config.DEBUG

# ЗАМЕНИТЕ существующую функцию index() на эту:

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    mods = get_all_mods()
    all_tags = get_all_tags()
    
    mods_data = []
    for mod in mods:
        tags = get_tags_for_mod(mod[0])
        mods_data.append({
            'id': mod[0],
            'title': mod[1],
            'image': mod[2],
            'url': mod[3],
            'download_url': mod[4],
            'tags': [{'id': t[0], 'name': t[1]} for t in tags]
        })
        
    tags_data = [{'id': t[0], 'name': t[1], 'created_at': t[2]} for t in all_tags]
    
    return jsonify({
        'mods': mods_data,
        'tags': tags_data
    })

@app.route('/add', methods=['POST'])
def add_mod_route():
    data = request.get_json()
    url = data.get('mod_url', '').strip()
    
    if not url.startswith('https://sims-market.ru/mod/'):
        return jsonify({'success': False, 'message': "Неверный URL! Должен начинаться с https://sims-market.ru/mod/"})
    
    try:
        mod_data = parse_mod_data(url)
        add_mod(mod_data)
        return jsonify({'success': True, 'message': f"Мод '{mod_data['title']}' успешно добавлен!"})
    except Exception as e:
        return jsonify({'success': False, 'message': f"Ошибка при добавлении мода: {str(e)}"})

@app.route('/delete/<int:mod_id>', methods=['POST'])
def delete_mod_route(mod_id):
    try:
        delete_mod(mod_id)
        return jsonify({'success': True, 'message': "Мод удален"})
    except Exception as e:
        return jsonify({'success': False, 'message': f"Ошибка при удалении: {str(e)}"})

@app.route('/tags')
def tags_page():
    return render_template('tags.html')

@app.route('/api/tags')
def get_tags_api():
    tags = get_all_tags()
    tags_data = [{'id': t[0], 'name': t[1], 'created_at': t[2]} for t in tags]
    return jsonify({'tags': tags_data})

@app.route('/add_tag', methods=['POST'])
def add_tag_route():
    data = request.get_json()
    tag_name = data.get('tag_name', '').strip()
    try:
        add_tag(tag_name)
        return jsonify({'success': True, 'message': f"Тег '{tag_name}' успешно добавлен!"})
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/edit_tag/<int:tag_id>', methods=['POST'])
def edit_tag_route(tag_id):
    data = request.get_json()
    new_name = data.get('tag_name', '').strip()
    try:
        update_tag(tag_id, new_name)
        return jsonify({'success': True, 'message': "Тег успешно обновлен!"})
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'message': f"Ошибка: {str(e)}"})

@app.route('/delete_tag/<int:tag_id>', methods=['POST'])
def delete_tag_route(tag_id):
    try:
        delete_tag(tag_id)
        return jsonify({'success': True, 'message': "Тег удален"})
    except Exception as e:
        return jsonify({'success': False, 'message': f"Ошибка при удалении: {str(e)}"})

@app.route('/health')
def health_check():
    """Эндпоинт для проверки состояния приложения"""
    try:
        # Проверяем подключение к БД
        conn = get_db_connection()
        conn.close()
        status = "OK"
        db_status = "Connected"
    except Exception as e:
        status = "ERROR"
        db_status = str(e)
    
    return {
        "status": status,
        "environment": config.FLASK_ENV,
        "database_type": config.DATABASE_TYPE,
        "database_status": db_status,
        "debug_mode": app.debug
    }, 200 if status == "OK" else 500

@app.route('/mod/<int:mod_id>/add_tag/<int:tag_id>', methods=['POST'])
def add_tag_to_mod_route(mod_id, tag_id):
    try:
        add_tag_to_mod(mod_id, tag_id)
        all_tags = get_all_tags()
        tag_name = next((tag[1] for tag in all_tags if tag[0] == tag_id), "Неизвестный тег")
        return jsonify({
            'success': True,
            'message': f'Тег "{tag_name}" добавлен к моду',
            'tag_id': tag_id,
            'tag_name': tag_name
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/mod/<int:mod_id>/remove_tag/<int:tag_id>', methods=['POST'])
def remove_tag_from_mod_route(mod_id, tag_id):
    try:
        remove_tag_from_mod(mod_id, tag_id)
        return jsonify({'success': True, 'message': 'Тег удален'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    init_db()
    
    PORT = 7066
    HOST = '0.0.0.0'
    
    print(f"🚀 Запуск приложения в режиме: {config.FLASK_ENV}")
    print(f"🗃️  Тип базы данных: {config.DATABASE_TYPE}")
    
    if config.FLASK_ENV == 'development':
        print("💡 Совет: Для запуска в продакшене используйте:")
        print("   FLASK_ENV=production DATABASE_TYPE=mysql python app.py")
    
    app.run(host=HOST, 
            port=PORT,
            debug=config.DEBUG)