from celery import Celery
from efimera import create_app

def create_celery():
    app = create_app()
    celery = Celery(app.import_name)
    
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = create_celery()

