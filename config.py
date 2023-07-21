import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:Horizon2021@localhost:3308/akasiatest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False