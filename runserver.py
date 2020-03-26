from login.login import *  # 调用登录模块
from order.add_order import *  # 调用增加订单模块
from order.get_orderlist import *  # 调用获取订单列表模块
from application import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
    # app.run(host='172.20.10.2', port=8081,debug=True)