
def get_total_money(query_type, money_type, flag):
    overview = {
        "total_money": 0,
        "total_profit": 0,
        "total_post": 0
    }
    num = money_type.query.count()
    # 计算库存总金额
    for index in range(1, num + 1):
        money_data = money_type.query.get(index)
        # flag = isSold/isActive 标志stock/order
        if flag == 'stock':
            if int.from_bytes(query_type.isSold, byteorder='big') == 0:
                overview['total_money'] = overview['total_money'] + money_data.total
        elif flag == 'order':
            if int.from_bytes(query_type.isActive, byteorder='big') == 1:
                overview['total_money'] = overview['total_money'] + money_data.soldPrice
                overview['total_profit'] = overview['total_profit'] + money_data.profit
                overview['total_post'] = overview['total_post'] + money_data.postPrice
    return overview


def money_detail(order, order_money, stock, stock_money):
    order_result = order.query.filter_by('dateTime')




