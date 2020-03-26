from flask import request
import json
from order.order_database import Order, Money, Buyer, add_object
from application import app

@app.route("/api/add_order", methods=["POST"])
def add_order():
    '''
        This is the insert order API
        Call this api to insert order
        ---
        tags:
         - AddOrder
        parameters:
         - name: user_id
           in: body
           type: integer
           required: true
           description: 插入订单人id
           example: 1
         - name: productType
           in: body
           type: string
           required: true
           description: 产品类型
           example: Phone
         - name: productName
           in: body
           type: string
           required: true
           description: 产品名称
           example: iPhone
         - name: withAccessories
           in: body
           type: Boolean
           required: true
           description: 是否需要配件
           example: 1
         - name: accessories
           in: body
           type: array
           required: true
           description: 具体配件列表
           example: ["充电器"]
         - name: ProductDescription
           in: body
           type: dict
           required: true
           description: 机器的详细描述（颜色，外观，内存，储存）
           example: {"color":"silver","outlook":"新","memory":"16G","storage":"1024"}
         - name: platform
           in: body
           type: string
           required: true
           description: 出售平台
           example: vx
         - name: purchasePrice
           in: body
           type: integer
           required: true
           description: 进价
           example: 1000
         - name: soldPrice
           in: body
           type: integer
           required: true
           description: 售价
           example: 2000
         - name: postPrice
           in: body
           type: integer
           required: true
           description: 邮费
           example: 10
         - name: purchaser
           in: body
           type: string
           required: true
           description: 购买人
           example: W
         - name: contact
           in: body
           type: string
           required: true
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
        order_info = request.get_json()
        # 获取order信息
        order_info = order_info.get('order')
        back_data = {
            'user_id': order_info.get('user_id'),
            'type': order_info.get('productType')[-1],
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
