from flask import request, Blueprint, current_app
import json
import datetime
from app.models.stock import Stock, StockMoney, Creator
from app.models.money import MoneyDetail
from app.database.stock import insert_stock, get_stock, edit_stock_info, get_all_stocks, get_stock_page
from app.database.stock import get_accessories_list
from app.database.order import add_object
from app.models.users import verify_token

stock_api = Blueprint('stock', __name__)


@stock_api.route("/addStock", methods=["POST"])
def add_stock():
    token = request.headers.get('token')
    user = verify_token(token)
    if user == None:
        return 'Bad Request', 400
    if user.role == 1:
        get_data = request.get_json()
        # 获取stock信息
        stock_info = get_data.get('stock')
        back_data = {
            'userId': get_data.get('userId'),
            'productType': stock_info.get('productType'),
            'productName': stock_info.get('productName'),
            'productDescription': stock_info.get('productDescription'),
            'platform': stock_info.get('platform'),
            'price': stock_info.get('money')['price'],
            'num': stock_info.get('money')['num'],
            'creator': stock_info.get('creator'),
            'contact': stock_info.get('contact'),
            'note': stock_info.get('note')
        }
        stock = Stock()
        stock_money = StockMoney()
        stock_creator = Creator()
        md = MoneyDetail()

        # 配置stock_info
        stock.userId = back_data['userId']
        stock.dateTime = datetime.datetime.now()
        # 将productType 以字符串存入
        product_type = ''
        for i in range(len(back_data['productType'])):
            product_type = product_type + str(back_data['productType'][i])
            if i != len(back_data['productType']) - 1:
                product_type = product_type + '/'

        stock.productType = product_type
        stock.productName = back_data['productName']
        stock.productDescription = str(back_data['productDescription'])
        stock.platform = back_data['platform']
        stock.note = back_data['note']
        stock.isSold = 0
        # 配置stock_money
        stock_money.price = back_data['price']
        stock_money.num = back_data['num']
        stock_money.total = stock_money.price * stock_money.num
        # 配置stock_creator
        stock_creator.creator = back_data['creator']
        stock_creator.contact = back_data['contact']

        try:
            insert_stock(stock, stock_money, stock_creator)

            # 配置资金流水
            md.moneyType = 1
            md.typeId = stock.id
            md.productType = product_type
            md.productName = back_data['productName']
            md.money = stock_money.total
            md.dateTime = datetime.datetime.now()
            add_object(md)

            back_json = {
                "status": "success"
            }
            current_app.logger.info('%s insert stock successfully', back_data['productName'])
        except:
            # TODO 错误之后数据库的id问题
            back_json = {
                "status": "failed"
            }
            current_app.logger.error('创建库存发生错误')
    else:
        back_json = {
            "status": "forbid"
        }
    return json.dumps(back_json), 200


@stock_api.route("/getStockInfo", methods=["POST"])
def get_stock_info():
    data = request.get_json()
    stock_id = data.get("stockId")
    back_data = {
        "stock": get_stock(stock_id)
    }

    if back_data['stock'] != 'failed':
        return json.dumps(back_data)
    else:
        back_json = {
            "status": "failed",
            "reason": "库存不存在"
        }
        return json.dumps(back_json), 404


@stock_api.route("/editStockInfo", methods=["PUT"])
def edit_stock():
    token = request.headers.get('token')
    user = verify_token(token)
    if user == None:
        return 'Bad Request', 400

    if user.role == 1:
        # 修改库存信息
        get_data = request.get_json()
        result = edit_stock_info(get_data)

        if result == 1:
            back_json = {
                "status": "success"
            }
        else:
            back_json = {
                "status": "failed",
                "reason": "修改库存失败"
            }
    else:
        back_json = {
            "status": "forbid",
            "reason": "Without permission"
        }
    return json.dumps(back_json), 200


@stock_api.route("/getStocks", methods=["POST"])
def get_stock_list():
    page = request.get_json()
    page = int(page.get('page'))

    stock = Stock
    stock_money = StockMoney
    stock_creator = Creator

    back_json = get_all_stocks(stock, stock_money, stock_creator, page)

    return json.dumps(back_json), 200


@stock_api.route("/stock", methods=["GET"])
def stock_homepage():
    stock = Stock()
    money = StockMoney()
    type_dict = {
        "overview": {
            "num": 0,
            "total": 0
        },
        "types": ["Phone", "Pad", "Computer", "Accessories", "EarPhones", "Other"],
        "num": [0, 0, 0, 0, 0, 0],
        "total": [0, 0, 0, 0, 0, 0]
        }
    type_dict = get_stock_page(stock, money, type_dict)
    return json.dumps(type_dict), 200


# 获取配件列表
@stock_api.route("/getAccessories", methods=["GET"])
def select_accessories():
    accessories_list = get_accessories_list()
    back_json = {
        "accessoriesList": accessories_list,
        "num": len(accessories_list)
    }

    return json.dumps(back_json), 200


