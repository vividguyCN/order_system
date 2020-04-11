from app.models.order import Order
from app.models.stock import Stock


def get_total_money(query_type, money_type, flag):
    overview = {
        "total_money": 0,
        "total_profit": 0,
        "total_post": 0
    }
    num = money_type.query.count()
    # 计算库存总金额
    for index in range(1, num + 1):
        query_data = query_type.query.get(index)
        money_data = money_type.query.get(index)
        # flag = isSold/isActive 标志stock/order
        if flag == 'stock':
            if int.from_bytes(query_data.isSold, byteorder='big') == 0:
                overview['total_money'] = overview['total_money'] + money_data.total
        elif flag == 'order':
            if int.from_bytes(query_data.isActive, byteorder='big') == 1:
                overview['total_money'] = overview['total_money'] + money_data.soldPrice
                overview['total_profit'] = overview['total_profit'] + money_data.profit
                overview['total_post'] = overview['total_post'] + money_data.postPrice
    return overview


def get_time(elem):
    return elem.dateTime


def get_money_detail(order_money, stock_money, page):
    page_size = 50
    # 对result中数据按time倒序
    order_result = Order.query.filter_by(isActive=1).all()
    stock_result = Stock.query.filter_by(isSold=0).all()
    result = order_result + stock_result
    # result中数据为按照time倒序的所有有效的订单和库存数据
    result.sort(reverse=True, key=get_time)

    num = len(result)
    back_data = {
        "moneyDetail": [],
        "num": num
    }
    # 计算显示片段
    if num > page_size:
        # 有多页
        start = (page - 1) * page_size
        end = start + 49
        if end > num:
            end = num
    else:
        start = 0
        end = num
    detail = dict()
    for i in range(start, end):
        if type(result[i]) == Order:
            money = order_money.query.get(result[i].id).soldPrice
            detail['type'] = "out"
        elif type(result[i]) == Stock:
            money = stock_money.query.get(result[i].id).total
            detail['type'] = "in"
        detail = {
            "dateTime": str(result[i].dateTime),
            "productType": result[i].productType,
            "productName": result[i].productName,
            "money": money
        }
        back_data['moneyDetail'].append(detail)

    return back_data
