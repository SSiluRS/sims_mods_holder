from flask import Flask
from backend.config import get_config
from backend.app.database import init_db

def create_app(config_class=None):
    app = Flask(__name__)
    config = get_config()
    app.secret_key = config.SECRET_KEY
    app.debug = config.DEBUG
    
    # Initialize DB
    init_db() 
    
    from backend.app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app