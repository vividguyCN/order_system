from datetime import timedelta
import os

# BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# 定义配置基类
class Config:
    # 秘钥
    SECRET_KEY = os.urandom(24)  # 使用一组随机数对session进行加密
    # 数据库公用配置
    # 无警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 查询时显示原始的sql语句
    SQLALCHEMY_ECHO = False
    # session配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # 修改session 过期时间 --> session.permanent = True

    # 额外的初始化操作
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    HOSTNAME = 'localhost'
    PORT = '3306'
    DATABASE = 'order_system'
    USERNAME = 'root'
    PASSWORD = '123456'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI


# 测试环境配置
class TestConfig(Config):
    HOSTNAME = 'dmysql'
    PORT = '3306'
    DATABASE = 'order_system'
    USERNAME = 'root'
    PASSWORD = '123456'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI


# 生成一个字典，用来根据字符串找到对应的配置类。
config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'default': TestConfig
}