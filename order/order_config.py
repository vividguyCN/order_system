import os

# 配置数据库
DEBUG = True
SQLALCHEMY_ECHO = False

SECREET_KEY = os.urandom(24)
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'order_info'
USERNAME = 'root'
PASSWORD = '123'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI



