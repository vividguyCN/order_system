from flask import request
import json
from order_app import app
from flasgger import Swagger
from order_database import Order, Money, Buyer, get_all_orders

Swagger(app)

@app.route("/api/get_order", methods=["POST"])
def add_order():
    '''
    Call this api to get all orders
    ---
    tags:
     - Get_Order API
    parameters:
     - name: page
       in: body
       type: integer
       required: true
       description: order page
       example: 1
    responses:
      200:
       description: get order success,back order list
       schema:
         $ref: "#/definitions/Order_List"

    definitions:
        Order_List:
          properties:
            name:
              type: string
              example: iPhone
            type:
              type: string
              example: Phone
            income:
              type: integer
              example: 1000
            sold:
              type: integer
              example: 2000
            post:
              type: integer
              example: 10
            profit:
              type: integer
              example: 990
            purchaser:
              type: string
              example: H
            contact:
              type: string
              example: 182****9597

    '''
    if request.method == "POST":
        # 前端怎么发送page?
        page = request.get_json()
        page = int(page.get('page'))

        order = Order()
        money = Money()
        buyer = Buyer()

        order_list = get_all_orders(order,money,buyer,page)

    return json.dumps(order_list),200


app.run(host="0.0.0.0", port=3000, debug=True)