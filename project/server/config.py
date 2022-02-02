import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql:///' #'sqlite:///' 
database_name = 'diagnostic'
user = 'pwcbilvuomyhps'
password = '9b7848cd8db818bde579bb007b73a11ba025ada7a6ce377963f58d7c85832f3c'
alch_uri = 'postgres://pwcbilvuomyhps:9b7848cd8db818bde579bb007b73a11ba025ada7a6ce377963f58d7c85832f3c@ec2-107-20-153-39.compute-1.amazonaws.com:5432/dbn5l2onl9kdq4'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'diagnostic_secret')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = alch_uri



class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = alch_uri
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'diagnostic_secret'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = alch_uri
