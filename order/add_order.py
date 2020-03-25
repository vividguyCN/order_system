from flask import request
import json
from order_app import app
from flasgger import Swagger, swag_from
from order_database import Order, Money, Buyer, add_object

Swagger(app)

@app.route("/api/add_order", methods=["POST"])
def add_order():
    '''
    This is the insert order API
    Call this api to insert order
    ---
    tags:
     - Add_Order API
    parameters:
     - name: user_id
       in: body
       type: integer
       required: true
       description: who insert this order
       example: 1
     - name: type
       in: body
       type: string
       required: true
       description: order type
       example: Phone
     - name: name
       in: body
       type: string
       required: true
       description: name
       example: iPhone
     - name: accessories
       in: body
       type: Boolean
       required: true
       description: need accessories
       example: 1
     - name: sku
       in: body
       type: string
       required: true
       description: A detailed description of the machine（store,memory,color,outlook)
       example: black,A+,256
     - name: platform
       in: body
       type: string
       required: true
       description: sold platform
       example: vx
     - name: income
       in: body
       type: integer
       required: true
       description: income price
       example: 1000
     - name: sold
       in: body
       type: integer
       required: true
       description: sole price
       example: 2000
     - name: post
       in: body
       type: integer
       required: true
       description: post price
       example: 10
     - name: purchaser
       in: body
       type: string
       required: true
       description: who buy this
       example: W
     - name: contact
       in: body
       type: string
       required: true
       description: telephone number
       example: 182****9597
    responses:
      200:
       description: insert order success
      502:
       description: insert order failed
    '''
    if request.method == "POST":
        order_info = request.get_json()
        back_data = {
            'user_id': order_info.get('user_id'),
            'type': order_info.get('productType'),
            'name': order_info.get('productName'),
            'accessories': order_info.get('withAccessories'),
            'sku': order_info.get('productDescription'),
            'platform': order_info.get('platform'),
            'income': order_info.get('money')['incomePrice'],
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
        order.type = back_data['type'][-1]
        order.name = back_data['name']
        order.accessories = back_data['accessories']
        order.sku = str(back_data['sku']['storage']) + str(back_data['sku']['color']) + str(back_data['sku']['outlook'])
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

    return json.dumps(back_data),200


app.run(host="0.0.0.0", port=3000, debug=True)