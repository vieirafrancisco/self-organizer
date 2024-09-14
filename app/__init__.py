from flask import Flask

from .settings import SECRET_KEY


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['IPYTHON_CONFIG'] = {
        'InteractiveShell': {
            'colors': 'Linux',
            'confirm_exit': False,
        },
    }

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
