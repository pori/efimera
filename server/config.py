import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretsauce')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/efimera')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY = dict(
        broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        task_ignore_result=True
    )

     
class TestConfig:
    TEST = True
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/efimera')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
