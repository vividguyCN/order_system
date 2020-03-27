from flask import request
import json
import datetime
from order.order_database import Order, Money, Buyer, add_object
from application import app

@app.route("/api/AddOrder", methods=["POST"])
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
            'user_id': get_data.get('userId'),
            'type': order_info.get('productType')[0],
            'name': order_info.get('productName'),
            'withAccessories': order_info.get('withAccessories'),
            'description': order_info.get('productDescription'),
            'platform': order_info.get('platform'),
            'income': order_info.get('money')['purchasePrice'],
            'sold': order_info.get('money')['soldPrice'],
            'post': order_info.get('money')['postPrice'],
            'purchaser': order_info.get('purchaser'),
            'contact': order_info.get('contact'),
            'remark': order_info.get('note')
        }
        order = Order()
        money = Money()
        buyer = Buyer()

        # TODO user_id 从前端获取
        order.user_id = back_data['user_id']
        order.time = datetime.datetime.now()
        order.type = back_data['type']
        order.name = back_data['name']

        # 如果包含配件 加入配件字段
        # TODO 可能需要处理配件数组
        order.withAccessories = back_data['withAccessories']
        if(back_data['withAccessories']):
            accessories = ''
            for i in range(len(order_info.get('accessories'))):
                accessories = accessories + str(order_info.get('accessories')[i])
            order.accessories = accessories

        # 构造sku函数（获取产品的详细描述
        color = back_data['description']['color']
        outlook = back_data['description']['outlook']
        memory = back_data['description']['memory']
        storage = back_data['description']['storage']
        order.sku = str(color) + ',' + str(outlook) + ',' + str(memory) + ',' + str(storage)

        order.platform = back_data['platform']
        order.remark = back_data['remark']
        order.isActive = 1

        money.income = back_data['income']
        money.sold = back_data['sold']
        money.post = back_data['post']
        money.profit = money.sold - money.income - money.post

        buyer.name = back_data['purchaser']
        buyer.contact = back_data['contact']

        # TODO 增加异常处理（数据库回滚）,增加insert失败
        add_object(order, money, buyer)
        back_json = {
            "status": "success"
        }

    return json.dumps(back_json),200
