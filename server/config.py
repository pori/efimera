import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretsauce')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/efimera')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY = dict(
        broker_url = os.getenv('CELERY_BROKER_URL', 'redis://cache'),
        result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://cache'),
        task_ignore_result=True
    )

     
class TestConfig:
    TEST = True
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/efimera')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
