from app.models.order import Order
from app.models.stock import Stock
from datetime import datetime, timedelta


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


def get_money_detail(md, page, time_span):
    page_size = 50

    result = md.query.filter_by().all()

    num = len(result)
    back_data = {
        "moneyDetail": [],
        "num": 0,
        "in_money": 0,
        "out_money": 0
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

    # 加入时间约束
    end_time = datetime.now()
    if time_span == 'all':
        start_time = datetime.strptime('2016-5-24 00:00:00', '%Y-%m-%d %H:%M:%S')
    elif time_span == 'w':
        start_time = datetime.now() - timedelta(days=7)
    elif time_span == 'm':
        start_time = datetime.now().replace(day=1)

    # 计算total money
    out_money = 0
    in_money = 0

    for i in length:
        if result[i].dateTime < start_time or result[i].dateTime > end_time:
            continue
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
                in_money = in_money + detail['money']
            else:
                continue
        elif order_or_stock == 1:
            detail['type'] = "out"
            out_money = out_money + detail['money']

        back_data['moneyDetail'].append(detail)

    back_data['num'] = len(back_data['moneyDetail'])
    back_data['in_money'] = in_money
    back_data['out_money'] = out_money

    return back_data
