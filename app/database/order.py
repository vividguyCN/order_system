import datetime
from app.common import db
from app.models.order import Order, OrderMoney, Buyer
from app.models.stock import Stock, StockMoney


# 新增订单
def add_object(order, money, buyer):
    db.session.add(order)
    db.session.add(money)
    db.session.add(buyer)
    db.session.commit()
    print("add %r " % order.__repr__)
    print("add %r " % money.__repr__)
    print("add %r " % buyer.__repr__)


def get_all_orders(order, money, buyer, page):
    # 获得订单列表
    order_list = []

    num = order.query.count()
    total = order.query.filter_by(isActive=1).count()

    if num > 50:
        start = num - page * 50 + 1
        if start < 0:
            start = 1
        end = num - (page - 1) * 50
        # num = end - start + 1
    else:
        start = 1
        end = num

    length = range(end, start - 1, -1)  # 逆序
    for i in length:
        order_data = order.query.get(i)
        money_data = money.query.get(i)
        buyer_data = buyer.query.get(i)

        if order_data == None or int.from_bytes(order_data.isActive, byteorder='big') == 0:
            continue

        data = {
            "orderId": order_data.id,
            "dateTime": str(order_data.dateTime),
            "productName": order_data.productName,
            "productType": order_data.productType.split('/'),
            "productDescription": eval(order_data.productDescription),
            "purchasePrice": money_data.purchasePrice,
            "soldPrice": money_data.soldPrice,
            "postPrice": money_data.postPrice,
            "profit": money_data.profit,
            "purchaser": buyer_data.purchaser,
            "contact": buyer_data.contact,
            "platform": order_data.platform,
        }
        if order_data.accessories != None:
            data['accessories'] = order_data.accessories.split('/')
        if order_data.note != '':
            data['note'] = order_data.note

        # 在server层转换json会在结果中多出很多\
        # data_json = json.dumps(data)
        order_list.append(data)

    back_data = {
        'orderList': order_list,
        'total': total
    }
    return back_data


def get_order(order_id):
    # 获取订单详情
    order = Order.query.get(order_id)
    money = OrderMoney.query.get(order_id)
    purchaser = Buyer.query.get(order_id)
    is_active = int.from_bytes(order.isActive, byteorder='big')

    if is_active:
        back_data = {
            "productType": order.productType.split('/'),
            "productName": order.productName,
            "withAccessories": int.from_bytes(order.withAccessories, byteorder='big'),
            "productDescription": eval(order.productDescription),
            "platform": order.platform,
            "note": order.note,
            "money": {
                "purchasePrice": money.purchasePrice,
                "soldPrice": money.soldPrice,
                "postPrice": money.postPrice,
            },
            "purchaser": purchaser.purchaser,
            "contact": purchaser.contact
        }
        if back_data["withAccessories"]:
            back_data["accessories"] = order.accessories.split('/')
        return back_data
    else:
        return 'failed'


def delete_order(order_id):
    order = Order.query.get(order_id)
    order.isActive = 0
    return 1


def edit_order_info(data):
    order_id = data.get('orderId')
    order = Order.query.get(order_id)
    money = OrderMoney.query.get(order_id)
    buyer = Buyer.query.get(order_id)

    order_info = data.get('order')
    back_data = {
        "userId": data.get('userId'),
        "productType": order_info.get('productType'),
        "productName": order_info.get('productName'),
        "withAccessories": order_info.get('withAccessories'),
        "productDescription": order_info.get('productDescription'),
        "platform": order_info.get('platform'),
        "purchasePrice": order_info.get('money')['purchasePrice'],
        "soldPrice": order_info.get('money')['soldPrice'],
        "postPrice": order_info.get('money')['postPrice'],
        "purchaser": order_info.get('purchaser'),
        "contact": order_info.get('contact'),
        "note": order_info.get('note')
    }
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

    db.session.commit()
    return 1


def stock_2_order(stock_data):
    order = Order()
    order_money = OrderMoney()
    order_buyer = Buyer()
    stock = Stock.query.get(stock_data['stockId'])
    stock_money = StockMoney.query.get(stock_data['stockId'])

    # 修改库存
    sold_num = stock_data['num']
    if sold_num > stock_money.num:
        return 0
    if stock_money.num - sold_num <= 0:
        stock_money.num = 0
        stock.isSold = 1
    else:
        stock_money.num = stock_money - sold_num

    order.productType = stock.productType
    order.dateTime = stock_data['dataTime']
    order.productDescription = stock.productDescription
    order.userId = stock_data['userId']
    order.productName = stock.productName
    order.platform = stock_data['platform']
    order.note = stock_data['note']
    order.isActive = 1

    order_money.soldPrice = stock_data['soldPrice']
    order_money.purchasePrice = stock_money.price
    order_money.postPrice = stock_data['postPrice']
    order_money.profit = order_money.soldPrice - order_money.postPrice - order_money.purchasePrice

    order_buyer.purchaser = stock_data['purchaser']
    order_buyer.contact = stock_data['contact']

    add_object(order, order_money, order_buyer)
    return 1