from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        # Import the routes blueprint and register it with the app
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)

        db.create_all()

    return app
