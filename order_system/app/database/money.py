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


def get_money_detail(md, page):
    page_size = 50

    result = md.query.filter_by().all()

    num = len(result)
    back_data = {
        "moneyDetail": [],
        "num": num
    }
    if num > page_size:
        start = num - page * page_size - 1
        if start < 0:
            start = 1
        end = num - (page - 1) * page_size - 1
        # num = end - start + 1
    else:
        start = -1
        end = num - 1

    length = range(end, start, -1)  # 逆序

    for i in length:
        detail = {
            "dateTime": str(result[i].dateTime),
            "productType": result[i].productType.split('/'),
            "productName": result[i].productName,
            "money": result[i].money
        }
        order_or_stock = int.from_bytes(result[i].moneyType, byteorder='big')
        if order_or_stock == 0:
            order_data = Order.query.get(result[i].typeId)
            flag = int.from_bytes(order_data.isActive, byteorder='big')
            # 如果订单有效
            if flag == 1:
                detail['type'] = "in"
            else:
                continue
        elif order_or_stock == 1:
            detail['type'] = "out"

        back_data['moneyDetail'].append(detail)
    return back_data
