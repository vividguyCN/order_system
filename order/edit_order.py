from flask import request, session
import json
from order.order_database import get_order, delete_order
from application import app
import logging


@app.route("/api/getOrderInfo", methods=["PUT"])
def get_order_info():
    """
    This is the GetOrderInfo API
    ---
    tags:
      - GetOrderInformation
    put:
      parameters:
        - name: orderId
          in: body
          type: string
          required: true
          description: 订单id
          example: 1
    responses:
        200:
          description: 返回订单信息
          schema:
            type:
              object
            example:
              {"productType": ["Accessories", "Android", "Noise"], "productName": "iPad pro 12.9", "withAccessories": 1,
"productDescription": "{'color': 'green', 'outlook': '\u5168\u65b0', 'memory': '8G', 'storage': '64G'}", "platform":
"xy", "note": "", "money": {"purchasePrice": 1289, "soldPrice": 2105, "postPrice": 11}, "purchaser": "\u738b\u4e94",
"contact": "10086", "accessories": ["Charger"]}
    """
    data = request.get_json()
    order_id = data.get("orderId")
    back_data = get_order(order_id)

    if back_data != 'failed':
        return json.dumps(back_data)
    else:
        return '订单不存在', 500


@app.route("/api/delOrder", methods=["DELETE"])
def del_order():
    """
    This is the DeleteOrder API
    ---
    tags:
      - DeleteOrder
    delete:
      parameters:
        - name: orderId
          in: body
          type: string
          required: true
          description: 订单id
          example: 1
    responses:
        200:
          description: 返回订单信息
          schema:
            status:
            type:
              object
            example:
              success
    """
    data = request.get_json()
    order_id = data.get('orderId')
    delete_order(order_id)
    back_json = {
        "status": "success"
    }

    return json.dumps(back_json), 200

