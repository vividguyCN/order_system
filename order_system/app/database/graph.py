from order_system.app.models.order import Order, OrderMoney
import datetime
from sqlalchemy import and_


def c_profit(order):
    num = len(order)
    profit = 0
    for i in range(num):
        money = OrderMoney.query.get(order[i].id)
        profit = profit + money.profit
    return profit


def get_order_by_time(days, today):
    sales = []
    profit = []
    for i in range(days, 0, -1):
        start_day = today - datetime.timedelta(days=i)
        end_day = today - datetime.timedelta(days=i-1)
        result = Order.query.filter_by(isActive=1).filter(and_(Order.dateTime.__ge__(start_day), Order.dateTime.__le__(end_day))).all()
        daily_profit = c_profit(result)
        num = len(result)
        sales.append(num)
        profit.append(daily_profit)
    back_json = {
        "sales": sales,
        "profit": profit
    }

    return back_json
