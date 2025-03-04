from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# SQLAlchemy   

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
migrate = Migrate()


# Celery

from celery import Celery, Task

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()

    app.extensions["celery"] = celery_app

    return celery_app

