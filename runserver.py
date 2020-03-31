from login.login import *  # 调用登录模块
from order.add_order import *  # 调用增加订单模块
from order.get_orderlist import *  # 调用获取订单列表模块
from login.edit_user_info import *
from order.edit_order import *
from graph.graph import *
from application import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)