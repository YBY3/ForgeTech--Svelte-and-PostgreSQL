import os

DB_USERNAME = os.getenv('project_55_user')
DB_PASSWORD = os.getenv('project_55_password')
DB_HOST = '161.35.106.21'
DB_NAME = 'project_55_db'

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False