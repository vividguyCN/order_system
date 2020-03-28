from flask import request
import json
import datetime
from order.order_database import Order, Money, Buyer, add_object
from application import app


@app.route("/api/addOrder", methods=["POST"])
def add_order():
    '''
        This is the insert order API
        Call this api to insert order
        ---
        tags:
         - AddOrder
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
        responses:
          200:
           description: 插入订单成功，返回一个状态success
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
    '''
    if request.method == "POST":
        get_data = request.get_json()
        # 获取order信息
        order_info = get_data.get('order')
        back_data = {
            'userId': get_data.get('userId'),
            'productType': order_info.get('productType'),
            'productName': order_info.get('productName'),
            'withAccessories': order_info.get('withAccessories'),
            'productDescription': order_info.get('productDescription'),
            'platform': order_info.get('platform'),
            'purchasePrice': order_info.get('money')['purchasePrice'],
            'soldPrice': order_info.get('money')['soldPrice'],
            'postPrice': order_info.get('money')['postPrice'],
            'purchaser': order_info.get('purchaser'),
            'contact': order_info.get('contact'),
            'note': order_info.get('note')
        }
        order = Order()
        money = Money()
        buyer = Buyer()

        # TODO user_id 从前端获取
        order.userId = back_data['userId']
        order.dateTime = datetime.datetime.now()

        # 将productType 以字符串存入
        product_type = ''
        for i in range(len(back_data['productType'])):
            product_type = product_type + str(back_data['productType'][i])
            if i != len(back_data['productType']) - 1:
                product_type = product_type + '/'

        order.productType = product_type
        order.productName = back_data['productName']

        # 如果包含配件 加入配件字段
        order.withAccessories = back_data['withAccessories']
        if back_data['withAccessories']:
            accessories = ''
            for i in range(len(order_info.get('accessories'))):
                accessories = accessories + str(order_info.get('accessories')[i])
                if i != len(order_info.get('accessories')) - 1:
                    accessories = accessories + '/'
            order.accessories = accessories

        order.productDescription = str(back_data['productDescription'])

        order.platform = back_data['platform']
        order.note = back_data['note']
        order.isActive = 1

        money.purchasePrice = back_data['purchasePrice']
        money.soldPrice = back_data['soldPrice']
        money.postPrice = back_data['postPrice']
        money.profit = money.soldPrice - money.purchasePrice - money.postPrice

        buyer.purchaser = back_data['purchaser']
        buyer.contact = back_data['contact']

        # TODO 增加异常处理（数据库回滚）,增加insert失败
        add_object(order, money, buyer)
        back_json = {
            "status": "success"
        }

    return json.dumps(back_json),200
