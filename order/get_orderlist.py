from flask import request
import json
from order.order_database import Order, Money, Buyer, get_all_orders
from application import app


@app.route("/api/getOrder", methods=["POST"])
def get_order():
    '''
    Call this api to get all orders
    ---
    tags:
     - GetOrder
    parameters:
     - name: page
       in: body
       type: integer
       required: true
       description: 订单列表页数
       example: 1
    responses:
      200:
       description: 获取订单成功，返回一个列表，包含page中的订单
       schema:
         $ref: "#/definitions/OrderList"

    definitions:
        OrderList:
          properties:
            orderList:
              type: array
              example: [{"orderId": 1,"dateTime": "2020-03-27 02:38:47","productName": "iPhone","productType": ["Phone","Apple"],"productDescription": {"color":"sliver","outlook":"全新"}, "purchasePrice": 1000,"soldPrice": 2000,"postPrice": 20,"profit": 980,"platform":"vx","purchaser": "张三","contact": 182****9597}]
            total:
              type: integer
              example: 1
    '''
    if request.method == "POST":
        page = request.get_json()
        page = int(page.get('page'))

        order = Order()
        money = Money()
        buyer = Buyer()

        order_list = get_all_orders(order,money,buyer,page)
        back_json = {
            'orderList': order_list
        }

    return json.dumps(back_json), 200
