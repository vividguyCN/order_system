from flask import request, Blueprint, current_app
import json
from app.database.order import *
from app.models.money import MoneyDetail

order_api = Blueprint('order', __name__)


@order_api.route("/addOtherOrder", methods=["POST"])
def add_other_order():
    if request.method == "POST":
        get_data = request.get_json()
        # 获取order信息
        order_info = get_data.get('order')
        back_data = {
            'userId': get_data.get('userId'),
            'productType': order_info.get('productType'),
            'productName': order_info.get('productName'),
            'productDescription': str(order_info.get('productDescription')),
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
        # 写入配件
        product_type = ''
        for i in range(len(back_data['productType'])):
            product_type = product_type + back_data['productType'][i]
            if i != len(back_data['productType']) - 1:
                product_type = product_type + '/'
        order.productType = product_type

        order.productName = back_data['productName']
        order.productDescription = str(back_data['productDescription'])
        order.platform = back_data['platform']
        order.stockId = 0
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
        add_object(order)
        add_object(money)
        add_object(buyer)
        # 资金流水加入
        md = MoneyDetail()
        md.dateTime = datetime.datetime.now()
        md.typeId = order.id
        md.moneyType = 0
        md.productType = product_type
        md.productName = back_data['productName']
        md.money = back_data['soldPrice']
        add_object(md)

        back_json = {
            "status": "success"
        }
    current_app.logger.info('%s 创建其他订单，产品:%s', back_data['userId'], back_data['productName'])
    return json.dumps(back_json),200


@order_api.route("/addStockOrder", methods=["POST"])
def add_stock_order():
    data = request.get_json()
    stock_data = data.get('stock')
    stock_data = {
        "stockId": data.get("stockId"),
        "userId": data.get('userId'),
        "soldPrice": stock_data.get("money")['soldPrice'],
        "postPrice": stock_data.get("money")['postPrice'],
        "num": stock_data.get('num'),
        "purchaser": stock_data.get('purchaser'),
        "contact": stock_data.get('contact'),
        "note": stock_data.get("note"),
        "dateTime": datetime.datetime.now(),
        "platform": stock_data.get('platform')
    }

    result = stock_2_order(stock_data)
    back_json = {
        "status": "failed"
    }
    if result == 0:
        back_json['reason'] = '库存不足'
    elif result == 1:
        back_json['status'] = 'success'
        current_app.logger.info("%s 创建库存订单 订单id: %s", stock_data['userId'], stock_data['stockId'])
    return json.dumps(back_json), 200


@order_api.route("/getOrderInfo", methods=["POST"])
def get_order_info():
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
    data = request.get_json()
    order_id = data.get('orderId')
    delete_order(order_id)
    back_json = {
        "status": "success"
    }
    current_app.logger.info('%s 订单删除成功', order_id)
    return json.dumps(back_json), 200


@order_api.route("/editOrderInfo", methods=["PUT"])
def edit_order():
    # 修改订单信息
    get_data = request.get_json()
    result = edit_order_info(get_data)

    if result == 1:
        back_json = {
            "status": "success"
        }
        current_app.logger.info('%s 修改订单成功', get_data.get('userId'))
    else:
        back_json = {
            "status": "failed",
            "reason": "修改订单失败"
        }
        current_app.logger.info('%s 修改订单失败', get_data.get('userId'))
    return json.dumps(back_json), 200


@order_api.route("/getOrders", methods=["POST"])
def get_order_list():
    if request.method == "POST":
        page = request.get_json()
        page = int(page.get('page'))

        order = Order()
        money = OrderMoney()
        buyer = Buyer()

        back_json = get_all_orders(order, money, buyer, page)

    return json.dumps(back_json), 200

