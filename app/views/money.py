from flask import Blueprint
import json
from app.database.money import get_total_money
from app.models.stock import StockMoney, Stock
from app.models.order import OrderMoney, Order

money_api = Blueprint('money', __name__)


@money_api.route("/money", methods=["GET"])
def money_homepage():
    """
    使用这个api来获取资金总览页面的表格
    ---
    tags:
     - MoneyHomePage
    responses:
      200:
       description: 获取图表成功,返回库存总金额，销售金额，盈利，邮费
       schema:
         $ref: "#/definitions/MoneyPage"

    definitions:
        MoneyPage:
          properties:
            stockMoney:
              type: integer
              example: 1000
            orderSold:
              type: integer
              example: 2000
            orderProfit:
              type: integer
              example: 500
            orderPost:
              type: integer
              example: 100
            orderPurchase:
              type: integer
              example: 1400
    """
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
