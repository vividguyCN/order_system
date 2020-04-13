from flask import Blueprint, request
import json
from app.database.money import get_total_money, get_money_detail
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


@money_api.route("/moneyDetail",methods=["POST"])
def money_detail():
    """
    使用这个api来获取资金流水明细
    ---
    tags:
     - MoneyDetail
    responses:
      200:
       description: 返回资金流水列表
       schema:
         $ref: "#/definitions/MoneyDetail"

    definitions:
        MoneyDetail:
          properties:
            moneyDetail:
              type: array
              example: [{"type":"in","dateTime":"2020-04-11 01:21:39","productType":["Pad"],"productName":"iPad",
              "money":"4000"}]
            num:
              type: integer
              example: 1

    """
    data = request.get_json()
    page = int(data.get('page'))

    order_money = OrderMoney()
    stock_money = StockMoney()

    back_json = get_money_detail(order_money, stock_money, page)

    return json.dumps(back_json), 200
