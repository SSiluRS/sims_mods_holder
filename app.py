from flask import Flask, render_template, request, redirect, flash, url_for
from database import init_db, get_all_mods, add_mod, delete_mod, get_all_tags, add_tag, update_tag, delete_tag, get_tags_for_mod, add_tag_to_mod, remove_tag_from_mod
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
    mods = get_all_mods()
    all_tags = get_all_tags()
    
    # Получаем теги для каждого мода
    tags_for_mod = {}
    for mod in mods:
        tags_for_mod[mod[0]] = get_tags_for_mod(mod[0])
    
    return render_template('index.html', 
                         mods=mods, 
                         all_tags=all_tags, 
                         tags_for_mod=tags_for_mod,
                         current_filter_tag=None,  # Нет активного фильтра
                         current_filter_name=None)

@app.route('/add', methods=['POST'])
def add_mod_route():
    url = request.form.get('mod_url', '').strip()
    if not url.startswith('https://sims-market.ru/mod/'):
        flash("Неверный URL! Должен начинаться с https://sims-market.ru/mod/", "danger")
        return redirect('/')
    
    try:
        mod_data = parse_mod_data(url)
        add_mod(mod_data)
        flash(f"Мод '{mod_data['title']}' успешно добавлен!", "success")
    except Exception as e:
        flash(f"Ошибка при добавлении мода: {str(e)}", "danger")
    
    return redirect('/')

@app.route('/delete/<int:mod_id>', methods=['POST'])
def delete_mod_route(mod_id):
    try:
        delete_mod(mod_id)
        flash("Мод удален", "success")
    except Exception as e:
        flash(f"Ошибка при удалении: {str(e)}", "danger")
    return redirect('/')

@app.route('/tags')
def tags_page():
    tags = get_all_tags()
    return render_template('tags.html', tags=tags)

@app.route('/add_tag', methods=['POST'])
def add_tag_route():
    tag_name = request.form.get('tag_name', '').strip()
    try:
        add_tag(tag_name)
        flash(f"Тег '{tag_name}' успешно добавлен!", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for('tags_page'))

@app.route('/edit_tag/<int:tag_id>', methods=['POST'])
def edit_tag_route(tag_id):
    new_name = request.form.get('tag_name', '').strip()
    try:
        update_tag(tag_id, new_name)
        flash(f"Тег успешно обновлен!", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for('tags_page'))

@app.route('/delete_tag/<int:tag_id>', methods=['POST'])
def delete_tag_route(tag_id):
    try:
        delete_tag(tag_id)
        flash("Тег удален", "success")
    except Exception as e:
        flash(f"Ошибка при удалении: {str(e)}", "danger")
    return redirect(url_for('tags_page'))

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
        
        # Проверяем, это AJAX-запрос или обычный
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
           request.content_type == 'application/json':
            # AJAX-ответ
            all_tags = get_all_tags()
            tag_name = next((tag[1] for tag in all_tags if tag[0] == tag_id), "Неизвестный тег")
            return jsonify({
                'success': True,
                'message': f'Тег "{tag_name}" добавлен к моду',
                'tag_id': tag_id,
                'tag_name': tag_name
            })
        else:
            # Обычный редирект
            flash("Тег успешно добавлен к моду", "success")
            return redirect('/')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        else:
            flash(f"Ошибка: {str(e)}", "danger")
            return redirect('/')

@app.route('/mod/<int:mod_id>/remove_tag/<int:tag_id>', methods=['POST'])
def remove_tag_from_mod_route(mod_id, tag_id):
    try:
        remove_tag_from_mod(mod_id, tag_id)
        
        # Проверяем, это AJAX-запрос
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Тег удален'
            })
        else:
            flash("Тег удален из мода", "success")
            return redirect('/')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        else:
            flash(f"Ошибка: {str(e)}", "danger")
            return redirect('/')

@app.route('/filter_by_tag/<int:tag_id>')
def filter_by_tag(tag_id):
    # Получаем все моды и теги
    all_mods = get_all_mods()
    all_tags = get_all_tags()
    
    # Получаем моды, которые имеют указанный тег
    filtered_mods = []
    for mod in all_mods:
        mod_tags = get_tags_for_mod(mod[0])
        # Проверяем, есть ли у мода указанный тег
        if any(tag[0] == tag_id for tag in mod_tags):
            filtered_mods.append(mod)
    
    # Получаем имя тега для отображения
    tag_name = next((tag[1] for tag in all_tags if tag[0] == tag_id), "Неизвестный тег")
    
    # Подготавливаем теги для каждого мода (как в обычном маршруте)
    tags_for_mod = {}
    for mod in filtered_mods:
        tags_for_mod[mod[0]] = get_tags_for_mod(mod[0])
    
    return render_template('index.html', 
                         mods=filtered_mods,
                         all_tags=all_tags,
                         tags_for_mod=tags_for_mod,
                         current_filter_tag=tag_id,
                         current_filter_name=tag_name)

if __name__ == '__main__':
    init_db()
    print(f"🚀 Запуск приложения в режиме: {config.FLASK_ENV}")
    print(f"🗃️  Тип базы данных: {config.DATABASE_TYPE}")
    print(f"🔗 Адрес: http://localhost:5000")
    
    if config.FLASK_ENV == 'development':
        print("💡 Совет: Для запуска в продакшене используйте:")
        print("   FLASK_ENV=production DATABASE_TYPE=mysql python app.py")
    
    app.run(host='0.0.0.0' if config.FLASK_ENV == 'production' else '127.0.0.1', 
            port=7066 if config.FLASK_ENV == 'production' else 5000,
            debug=config.DEBUG)