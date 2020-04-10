from flask import request, Blueprint
import json
import datetime
from app.models.stock import Stock, StockMoney, Creator
from app.database.stock import insert_stock, get_stock, edit_stock_info, get_all_stocks, get_stock_page

stock_api = Blueprint('stock', __name__)


@stock_api.route("/addStock", methods=["POST"])
def add_stock():
    """
   使用这个api来添加库存
    ---
    tags:
     - AddStock
    parameters:
    parameters:
     - name: userId
       in: body
       type: integer
       required: true
       description: 创建库存人id
       example: 1
     - name: stock
       in: body
       type: object
       required: true
       description: 需要的库存数据
       properties:
            productType:
                type: array
                description: 产品类型
                example: ['Pad']
            productName:
                type: string
                description: 产品名称
                example: iPhone
            productDescription:
                type: object
                description: 机器的详细描述（颜色，外观，内存，储存）
                properties:
                    color:
                        type: string
                        description: 颜色
                        example: silver
                    outlook:
                        type: string
                        description: 外观
                        example: 新
                    memory:
                        type: string
                        description: 内存
                        example: 8G
                    storage:
                        type: string
                        description: 内存
                        example: 1024
            platform:
                type: string
                description: 收购平台
                example: vx
            money:
                type: object
                description: 钱
                properties:
                    price:
                        type: integer
                        description: 单价
                        example: 100
                    num:
                        type: integer
                        description: 数量
                        example: 20
            creator:
                type: string
                description: 创建人
                example: W
            contact:
                type: string
                description: 联系方式
                example: 182****9597
            note:
                type: string
                description: 备注
                example: admin
    responses:
      200:
       description: 创建库存成功，返回一个状态success
       schema:
         properties:
            status:
              type: string
              example: success
      502:
       description: 创建库存失败，返回一个状态failed
       schema:
         properties:
            status:
              type: string
              example: failed
    """
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

    # TODO 增加异常处理（数据库回滚）,增加insert失败
    insert_stock(stock, stock_money, stock_creator)
    back_json = {
        "status": "success"
    }
    # app.logger.info('%s insert order successfully', back_data['userId'])
    return json.dumps(back_json), 200


@stock_api.route("/getStockInfo", methods=["POST"])
def get_stock_info():
    """
   使用这个api来获取库存信息
    ---
    tags:
      - GetStockInformation
    post:
      parameters:
        - name: stockId
          in: body
          type: integer
          required: true
          description: 库存号
          example: 1
    responses:
        200:
          description: 返回的库存信息
          schema:
            type:
              object
            example:
              {"stock":{"productType": ["Accessories", "Android", "Noise"], "productName": "iPad pro 12.9",
"productDescription": {"color": "green", "outlook": "\u5168\u65b0", "memory": "8G", "storage": "64G"}, "platform":
"xy", "note": "", "money": {"price": 1289, "num": 2105, "total": 11}, "creator": "\u738b\u4e94",
"contact": "10086"}}
        404:
          description: 库存不存在
          schema:
            type: object
            example:
              {"status":"failed","reason":"库存不存在"}
    """
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
    """
    使用这个api来编辑库存信息
    ---
    tags:
     - EditStockInfo
    parameters:
     - name: stockId
       in: body
       type: integer
       required: true
       description: 库存号
       example: 1
     - name: userId
       in: body
       type: integer
       required: true
       description: 修改库存人id
       example: 1
     - name: stock
       in: body
       type: object
       required: true
       description: 需要的库存数据
       properties:
            productType:
                type: array
                description: 产品类型
                example: ['Pad']
            productName:
                type: string
                description: 产品名称
                example: iPhone
            productDescription:
                type: object
                description: 机器的详细描述（颜色，外观，内存，储存）
                properties:
                    color:
                        type: string
                        description: 颜色
                        example: silver
                    outlook:
                        type: string
                        description: 外观
                        example: 新
                    memory:
                        type: string
                        description: 内存
                        example: 8G
                    storage:
                        type: string
                        description: 内存
                        example: 1024
            platform:
                type: string
                description: 出售平台
                example: vx
            money:
                type: object
                description: 钱
                properties:
                    price:
                        type: integer
                        description: 单价
                        example: 100
                    num:
                        type: integer
                        description: 数量
                        example: 20
            creator:
                type: string
                description: 创建人
                example: W
            contact:
                type: string
                description: 联系方式
                example: 182****9597
            note:
                type: string
                description: 备注
                example: admin
    responses:
      200:
       description: 修改库存成功，返回一个状态success
       schema:
         properties:
            status:
              type: string
              example: success
      502:
       description: 修改库存失败，返回一个状态failed和reason
       schema:
         properties:
            status:
              type: string
              example: failed
            reason:
              type: string
              example: 修改库存失败
    """
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
    return json.dumps(back_json), 200


@stock_api.route("/getStock", methods=["POST"])
def get_stock_list():
    """
    使用这个api来获得库存列表
    ---
    tags:
     - GetStock
    parameters:
     - name: page
       in: body
       type: integer
       required: true
       description: 库存列表页数
       example: 1
    responses:
      200:
       description: 获取库存成功，返回一个列表，包含page中的库存
       schema:
         $ref: "#/definitions/OrderList"

    definitions:
        OrderList:
          properties:
            orderList:
              type: array
              example: [{"stockId": 1,"dateTime": "2020-03-27 02:38:47","productName": "iPhone","productType": ["Phone","Apple"],"productDescription": {"color":"sliver","outlook":"全新"}, "price": 1000,"num": 20,"total": 20000,"platform":"vx","creator": "张三","contact": 182****9597}]
            total:
              type: integer
              example: 1
    """
    page = request.get_json()
    page = int(page.get('page'))

    stock = Stock
    stock_money = StockMoney
    stock_creator = Creator

    back_json = get_all_stocks(stock, stock_money, stock_creator, page)

    return json.dumps(back_json), 200


@stock_api.route("/stock", methods=["GET"])
def stock_homepage():
    """
    使用这个api来获取库存总览图表
    ---
    tags:
     - GetStockHomePage
    responses:
      200:
       description: 获取图表成功，返回包含库存总额，总数和各个类别的库存总额和总数
       schema:
         $ref: "#/definitions/StockGraph"

    definitions:
        StockGraph:
          properties:
            overview:
              type: object
              example: {"num":0,"total":0}
            Phone:
              type: object
              example: {"num":0,"total":0}
            Pad:
              type: object
              example: {"num":0,"total":0}
            Computer:
              type: object
              example: {"num":0,"total":0}
            EarPhone:
              type: object
              example: {"num":0,"total":0}
            Other:
              type: object
              example: {"num":0,"total":0}
            Accessories:
              type: object
              example: {"num":0,"total":0}
    """
    stock = Stock()
    money = StockMoney()
    type_dict = {
        "overview":{
            "num": 0,
            "total": 0
        },
        "Phone": {
            "num": 0,
            "total": 0
        },
        "Pad": {
            "num": 0,
            "total": 0
        },
        "Computer": {
            "num": 0,
            "total": 0
        },
        "Accessories": {
            "num": 0,
            "total": 0
        },
        "EarPhone": {
            "num": 0,
            "total": 0
        },
        "Other": {
            "num": 0,
            "total": 0
        }
    }
    type_dict = get_stock_page(stock, money, type_dict)
    return json.dumps(type_dict)


