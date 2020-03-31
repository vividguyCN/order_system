from flask import request, session
import json
import datetime
from order.order_database import get_order, delete_order, edit_order_info
from application import app
import logging


@app.route("/api/getOrderInfo", methods=["POST"])
def get_order_info():
    """
    This is the GetOrderInfo API
    ---
    tags:
      - GetOrderInformation
    post:
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
              {"order::{"productType": ["Accessories", "Android", "Noise"], "productName": "iPad pro 12.9", "withAccessories": 1,
"productDescription": "{'color': 'green', 'outlook': '\u5168\u65b0', 'memory': '8G', 'storage': '64G'}", "platform":
"xy", "note": "", "money": {"purchasePrice": 1289, "soldPrice": 2105, "postPrice": 11}, "purchaser": "\u738b\u4e94",
"contact": "10086", "accessories": ["Charger"]}}
        500:
          description: 订单不存在
          schema:
            type: object
            example:
              {"status":"failed","reason":"订单不存在"}
    """
    data = request.get_json()
    order_id = data.get("orderId")
    back_data = {
        "order": get_order(order_id)
    }

    if back_data != 'failed':
        return json.dumps(back_data)
    else:
        back_json = {
            "status": "failed",
            "reason": "订单不存在"
        }
        return json.dumps(back_json), 500


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
           description: 删除订单成功，返回一个状态success
           schema:
             properties:
                status:
                  type: string
                  example: success
    """
    data = request.get_json()
    print(data)
    order_id = data.get('orderId')
    delete_order(order_id)
    back_json = {
        "status": "success"
    }

    return json.dumps(back_json), 200


@app.route("/api/editOrderInfo", methods=["PUT"])
def edit_order():
    """
    This is the edit order API
        Call this api to Edit Order Information
        ---
        tags:
         - EditOrderInfo
        parameters:
         - name: orderId
           in: body
           type: integer
           required: true
           description: 订单id
           example: 1
         - name: userId
           in: body
           type: integer
           required: true
           description: 修改订单人id
           example: 1
         - name: order
           in: body
           type: object
           required: true
           description: 需要的订单数据
           properties:
                productType:
                    type: array
                    description: 产品类型
                    example: ['Pad']
                productName:
                    type: string
                    description: 产品名称
                    example: iPhone
                withAccessories:
                    type: Boolean
                    description: 是否需要配件
                    example: 1
                accessories:
                    type: array
                    description: 具体配件列表
                    example: ["Mouse"]
                productDescription:
                    type: object
                    description: 机器的详细描述（颜色，外观，内存，储存）
                    properties:
                        color:
                            type: string
                            description: 颜色
                            example: silver
                        outlook:
                            type: string
                            description: 外观
                            example: 新
                        memory:
                            type: string
                            description: 内存
                            example: 8G
                        storage:
                            type: string
                            description: 内存
                            example: 1024
                platform:
                    type: string
                    description: 出售平台
                    example: vx
                money:
                    type: object
                    description: 钱
                    properties:
                        purchasePrice:
                            type: integer
                            description: 进价
                            example: 1000
                        soldPrice:
                            type: integer
                            description: 售价
                            example: 2000
                        postPrice:
                            type: integer
                            description: 邮费
                            example: 10
                purchaser:
                    type: string
                    description: 购买人
                    example: W
                contact:
                    type: string
                    description: 联系方式
                    example: 182****9597
                note:
                    type: string
                    description: 备注
                    example: vip客户
        responses:
          200:
           description: 修改订单成功，返回一个状态success
           schema:
             properties:
                status:
                  type: string
                  example: success
          502:
           description: 修改订单失败，返回一个状态failed
           schema:
             properties:
                status:
                  type: string
                  example: failed
                reason:
                  type: string
                  example: 修改订单失败

    """
    # 修改订单信息
    get_data = request.get_json()
    result = edit_order_info(get_data)

    if result == 1:
        back_json = {
            "status": "success"
        }
    else:
        back_json = {
            "status": "failed",
            "reason": "修改订单失败"
        }
    return json.dumps(back_json), 200

