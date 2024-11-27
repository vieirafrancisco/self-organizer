from flask import Flask

from .settings import SECRET_KEY, DATABASE_URL
from .models import db


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['IPYTHON_CONFIG'] = {
        'InteractiveShell': {
            'colors': 'Linux',
            'confirm_exit': False,
        },
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .data import data as data_blueprint
    app.register_blueprint(data_blueprint)

    return app
