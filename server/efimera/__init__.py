from flask import Flask
from flask_cors import CORS

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    from .extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp
    app.register_blueprint(bp)

    return app
