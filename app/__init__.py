from flask import Flask
from flasgger import Swagger
from app.config import config
from app.views import config_blueprint


def create_app(config_name):
    # 创建app实例对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config.get(config_name) or 'default')
    print(app.config)
    # 加载swagger
    Swagger(app)
    # 执行额外的初始化
    config.get(config_name).init_app(app)
    # 设置debug=True,让toolbar生效
    # app.debug=True
    # 加载扩展
    # config_extensions(app)
    # 配置蓝本
    config_blueprint(app)
    # 配置全局错误处理
    # config_errorhandler(app)

    # 返回app实例对象
    return app
