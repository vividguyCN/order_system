from flask import request, Blueprint
import json
from app.database.order import *

order_api = Blueprint('order', __name__)


@order_api.route("/addOtherOrder", methods=["POST"])
def add_other_order():
    """
    使用这个api来添加其他订单
    ---
    tags:
     - AddOtherOrder
    parameters:
     - name: userId
       in: body
       type: integer
       required: true
       description: 插入订单人id
       example: 1
     - name: order
       in: body
       type: object
       required: true
       description: 需要的订单数据
       properties:
            productType:
                type: string
                description: 产品类型
                example: 门票
            productName:
                type: string
                description: 产品名称
                example: 杰伦演唱会
            productDescription:
                type: string
                description: 产品描述
                example: 1999价位
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
       description: 插入其他订单成功，返回一个状态success
       schema:
         properties:
            status:
              type: string
              example: success
      502:
       description: 插入订单失败，返回一个状态failed
       schema:
         properties:
            status:
              type: string
              example: failed
    """
    if request.method == "POST":
        get_data = request.get_json()
        # 获取order信息
        order_info = get_data.get('order')
        back_data = {
            'userId': get_data.get('userId'),
            'productType': order_info.get('productType'),
            'productName': order_info.get('productName'),
            'productDescription': {
                "description": str(order_info.get('productDescription'))
                },
            'platform': order_info.get('platform'),
            'purchasePrice': order_info.get('money')['purchasePrice'],
            'soldPrice': order_info.get('money')['soldPrice'],
            'postPrice': order_info.get('money')['postPrice'],
            'purchaser': order_info.get('purchaser'),
            'contact': order_info.get('contact'),
            'note': order_info.get('note')
        }
        order = Order()
        money = OrderMoney()
        buyer = Buyer()

        order.userId = back_data['userId']
        order.dateTime = datetime.datetime.now()
        order.productType = back_data['productType']
        order.productName = back_data['productName']
        order.productDescription = str(back_data['productDescription'])
        order.platform = back_data['platform']
        order.note = back_data['note']
        order.isActive = 1
        # 订单金额
        money.purchasePrice = back_data['purchasePrice']
        money.soldPrice = back_data['soldPrice']
        money.postPrice = back_data['postPrice']
        money.profit = money.soldPrice - money.purchasePrice - money.postPrice
        # 购买者
        buyer.purchaser = back_data['purchaser']
        buyer.contact = back_data['contact']
        # TODO 增加异常处理（数据库回滚）,增加insert失败
        add_object(order, money, buyer)
        back_json = {
            "status": "success"
        }
    # app.logger.info('%s insert order successfully', back_data['userId'])
    return json.dumps(back_json),200


@order_api.route("/addStockOrder", methods=["POST"])
def add_stock_order():
    """
    使用这个api来添加库存订单
    ---
    tags:
     - AddStockOrder
    parameters:
     - name: userId
       in: body
       type: integer
       required: true
       description: 创建订单人id
       example: 1
     - name: stockId
       in: body
       type: integer
       required: true
       description: 库存号
       example: 1
     - name: money
       type: object
       in: body
       required: true
       description: 金额
       properties:
           soldPrice:
             type: integer
             description: 售价
             example: 100
           postPrice:
             type: integer
             description: 邮费
             example: 10
     - name: num
       in: body
       type: integer
       required: true
       description: 数量
       example: 1
     - name: purchaser
       in: body
       type: string
       required: true
       description: 购买人
       example: 张三
     - name: contact
       in: body
       type: string
       required: true
       description: 联系方式
       example: 182****1597
     - name: note
       in: body
       type: string
       description: 备注
       example: vip
     - name: platform
       in: body
       type: string
       description: 出售方式
       example: vx
    responses:
      200:
       description: 订单创建失败
       schema:
         properties:
            status:
              type: string
              example: failed
            reason:
              type: string
              example: 库存不足
    """
    data = request.get_json()
    stock_data = {
        "stockId": data.get("stockId"),
        "userId": data.get('userId'),
        "soldPrice": data.get("money")['soldPrice'],
        "postPrice": data.get("money")['postPrice'],
        "num": data.get('num'),
        "purchaser": data.get('purchaser'),
        "contact": data.get('contact'),
        "note": data.get("note"),
        "dataTime": datetime.datetime.now(),
        "platform": data.get('platform')
    }
    result = stock_2_order(stock_data)
    back_json = {
        "status": "failed"
    }
    if result == 0:
        back_json['reason'] = '库存不足'
    elif result == 1:
        back_json['status'] = 'success'
    return json.dumps(back_json), 200


@order_api.route("/getOrderInfo", methods=["POST"])
def get_order_info():
    """
    使用这个api来获取订单信息
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
              {"order":{"productType": ["Accessories", "Android", "Noise"], "productName": "iPad pro 12.9",
"productDescription": {"color": "green", "outlook": "\u5168\u65b0", "memory": "8G", "storage": "64G"}, "platform":
"xy", "note": "", "money": {"purchasePrice": 1289, "soldPrice": 2105, "postPrice": 11}, "purchaser": "\u738b\u4e94",
"contact": "10086"}}
        404:
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

    if back_data['order'] != 'failed':
        return json.dumps(back_data)
    else:
        back_json = {
            "status": "failed",
            "reason": "订单不存在"
        }
        return json.dumps(back_json), 404


@order_api.route("/delOrder", methods=["DELETE"])
def del_order():
    """
    使用这个api来删除订单
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


@order_api.route("/editOrderInfo", methods=["PUT"])
def edit_order():
    """
    使用这个api来编辑订单信息
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


@order_api.route("/getOrder", methods=["POST"])
def get_order_list():
    """
    使用这个api来获得订单列表
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
            order:
              type: array
              example: [{"orderId": 1,"dateTime": "2020-03-27 02:38:47","productName": "iPhone","productType": ["Phone","Apple"],"productDescription": {"color":"sliver","outlook":"全新"}, "purchasePrice": 1000,"soldPrice": 2000,"postPrice": 20,"profit": 980,"platform":"vx","purchaser": "张三","contact": 182****9597}]
            orderNum:
              type: integer
              example: 1
    """
    if request.method == "POST":
        page = request.get_json()
        page = int(page.get('page'))

        order = Order()
        money = OrderMoney()
        buyer = Buyer()

        back_json = get_all_orders(order, money, buyer, page)

    return json.dumps(back_json), 200

