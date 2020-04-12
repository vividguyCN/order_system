import datetime
from app.common import db
from app.models.stock import StockMoney, Stock, Creator


# 增加库存
def insert_stock(stock, stock_money, creator):
    db.session.add(stock)
    db.session.add(stock_money)
    db.session.add(creator)
    db.session.commit()
    print("add %r " % stock.__repr__)
    print("add %r " % stock_money.__repr__)
    print("add %r " % creator.__repr__)
    return 1


# 获取stock_info
def get_stock(stock_id):
    # 获取订单详情
    stock = Stock.query.get(stock_id)
    money = StockMoney.query.get(stock_id)
    creator = Creator.query.get(stock_id)
    is_sold = int.from_bytes(stock.isSold, byteorder='big')

    if not is_sold:
        back_data = {
            "productType": stock.productType.split('/'),
            "productName": stock.productName,
            "productDescription": eval(stock.productDescription),
            "platform": stock.platform,
            "note": stock.note,
            "money": {
                "price": money.price,
                "num": money.num,
            },
            "creator": creator.creator,
            "contact": creator.contact
        }
        return back_data
    else:
        return 'failed'


# 修改库存信息
def edit_stock_info(data):
    stock_id = data.get('stockId')
    stock = Stock.query.get(stock_id)
    money = StockMoney.query.get(stock_id)
    creator = Creator.query.get(stock_id)

    stock_info = data.get('stock')
    back_data = {
        "userId": data.get('userId'),
        "productType": stock_info.get('productType'),
        "productName": stock_info.get('productName'),
        "withAccessories": stock_info.get('withAccessories'),
        "productDescription": stock_info.get('productDescription'),
        "platform": stock_info.get('platform'),
        "price": stock_info.get('money')['price'],
        "num": stock_info.get('money')['num'],
        "creator": stock_info.get('creator'),
        "contact": stock_info.get('contact'),
        "note": stock_info.get('note')
    }
    stock.userId = back_data['userId']
    stock.dateTime = datetime.datetime.now()

    # 将productType 以字符串存入
    product_type = ''
    for i in range(len(back_data['productType'])):
        product_type = product_type + str(back_data['productType'][i])
        if i != len(back_data['productType']) - 1:
            product_type = product_type + '/'
    # stock information
    stock.productType = product_type
    stock.productName = back_data['productName']
    stock.productDescription = str(back_data['productDescription'])
    stock.platform = back_data['platform']
    stock.note = back_data['note']
    stock.isSold = 0
    # stock money
    money.price = back_data['price']
    money.num = back_data['num']
    money.total = money.price * money.num
    # stock creator
    creator.creator = back_data['creator']
    creator.contact = back_data['contact']
    # update database
    db.session.commit()
    return 1


def get_stock_num(stock):
    stock_num = {
        "num": stock.query.count(),
        "total": stock.query.filter_by(isSold=0).count()
    }
    return stock_num


# 获得库存列表
def get_all_stocks(stock, money, creator, page):
    # 获得订单列表
    stock_list = []

    stock_num = get_stock_num(stock)
    num = stock_num['num']
    total = stock_num['total']

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
        stock_data = stock.query.get(i)
        money_data = money.query.get(i)
        buyer_data = creator.query.get(i)

        if stock_data == None or int.from_bytes(stock_data.isSold, byteorder='big') == 1:
            continue

        data = {
            "stockId": stock_data.id,
            "dateTime": str(stock_data.dateTime),
            "productName": stock_data.productName,
            "productType": stock_data.productType.split('/'),
            "productDescription": eval(stock_data.productDescription),
            "price": money_data.price,
            "num": money_data.num,
            "total": money_data.total,
            "creator": buyer_data.creator,
            "contact": buyer_data.contact,
            "platform": stock_data.platform,
        }
        # 在server层转换json会在结果中多出很多\
        # data_json = json.dumps(data)
        stock_list.append(data)

    back_data = {
        'stockList': stock_list,
        'stockNum': total
    }
    return back_data


def get_stock_page(stock, money, type_dict):
    total_money = 0
    total_num = 0
    num = money.query.count()
    # 对没有出售的库存求总额和数量
    for index in range(1, num+1):
        money_data = money.query.get(index)
        stock_data = stock.query.get(index)
        if int.from_bytes(stock_data.isSold, byteorder='big') == 0:
            total_money = total_money + money_data.total
            total_num = total_num + money_data.num
            product_type = stock_data.productType.split('/')
            # 对不同的type进行统计
            if product_type[0] in type_dict['types']:
                p = type_dict["types"].index(product_type[0])
                type_dict['num'][p] = type_dict['num'][p] + money_data.num
                type_dict['total'][p] = type_dict['total'][p] + money_data.total

    type_dict['overview']['num'] = total_num
    type_dict['overview']['total'] = total_money
    return type_dict

