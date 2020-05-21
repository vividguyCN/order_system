from .order import order_api
from .user import user_api
from .stock import stock_api
# from .main import main
from .graph import graph_api
from .money import money_api

DEFAULT_BLUEPRINT = (
    # (main, ''),
    (order_api, '/api'),
    (user_api, '/api'),
    (graph_api, '/api'),
    (stock_api, '/api'),
    (money_api, '/api')

)


# 封装配置蓝本的函数
def config_blueprint(app):
    # 循环读取元组中的蓝本
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
