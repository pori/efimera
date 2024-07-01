import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretsauce')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/efimera')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    TEST = True
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/efimera')
    SQLALCHEMY_TRACK_MODIFICATIONS = False