from flask import Blueprint, request
import json
from app.database.money import get_total_money, get_money_detail
from app.models.stock import StockMoney, Stock
from app.models.order import OrderMoney, Order
from app.models.money import MoneyDetail

money_api = Blueprint('money', __name__)


@money_api.route("/money", methods=["GET"])
def money_homepage():
    stock = Stock()
    stock_money = StockMoney()
    order = Order()
    order_money = OrderMoney()

    stock_total_money = get_total_money(stock, stock_money, 'stock')['total_money']
    order_get_money = get_total_money(order, order_money, 'order')
    order_sold = order_get_money['total_money']
    order_profit = order_get_money['total_profit']
    order_post = order_get_money['total_post']
    order_purchase = order_sold - order_profit - order_post
    back_data = {
        "stockMoney": stock_total_money,
        "orderPurchase": order_purchase,
        "orderSold": order_sold,
        "orderProfit": order_profit,
        "orderPost": order_post
    }
    return json.dumps(back_data), 200


@money_api.route("/moneyDetail",methods=["POST"])
def money_detail():
    data = request.get_json()
    page = int(data.get('page'))

    md = MoneyDetail()

    back_json = get_money_detail(md, page)

    return json.dumps(back_json), 200
