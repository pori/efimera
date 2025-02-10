from flask import Flask
from flask_cors import CORS


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    from .extensions import db, ma, migrate, celery_init_app

    # Database
    db.init_app(app)
    migrate.init_app(app, db)

    # Schemas
    ma.init_app(app)

    # Queue
    celery_init_app(app)
    
    from .routes import bp
    app.register_blueprint(bp)

    return app
