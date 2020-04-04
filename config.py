import os

# 配置数据库
DEBUG = True
<<<<<<< HEAD
SQLALCHEMY_ECHO = False

SECREET_KEY = os.urandom(24)
HOSTNAME = 'localhost'
PORT = '3306'
DATEBASE = 'login'
USERNAME = 'root'
PASDWORD = '123'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASDWORD,HOSTNAME,PORT,DATEBASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
=======
SECREET_KEY = os.urandom(24)
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'order_system'
USERNAME = 'root'
PASSWORD = '123'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

>>>>>>> dev

# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI



