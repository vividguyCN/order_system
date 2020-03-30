from flask_sqlalchemy import SQLAlchemy
from application import app
from config import DB_URI

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app,use_native_unicode='utf8')


class Order(db.Model):
    # order info
    __tablename__ = 'info'
    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.Integer, unique=True)
    dateTime = db.Column(db.DateTime, unique=True)
    productType = db.Column(db.String(255),unique=True)
    productName = db.Column(db.String(255),unique=True)
    productDescription = db.Column(db.String(255),unique=True)
    withAccessories = db.Column(db.Integer, unique=True)
    accessories = db.Column(db.String(255),unique=True)
    platform = db.Column(db.String(255),unique=True)
    note = db.Column(db.String(255),unique=True)
    isActive = db.Column(db.Integer,unique=True)
    def __repr__(self):
        # 只返回订单id
        return '<Order id:%r name:%r sku:%r>' % (self.id,self.productName,self.productDescription)


class Money(db.Model):
    # order money
    _tablename_ = 'money'
    id = db.Column(db.Integer,primary_key=True)
    purchasePrice = db.Column(db.Integer, unique=True)
    soldPrice = db.Column(db.Integer, unique=True)
    postPrice = db.Column(db.Integer, unique=True)
    profit = db.Column(db.Integer, unique=True)
    def __repr__(self):
        return '<Money id:%r profit%r>' % (self.id,self.profit)


class Buyer(db.Model):
    # purchaser info
    __tablename__ = 'purchaser'
    id = db.Column(db.Integer, primary_key=True)
    purchaser = db.Column(db.String(255),unique=True)
    contact = db.Column(db.String(255),unique=True)
    def __repr__(self):
        return '<Purchaser name:%r contact:%r>' % (self.purchaser,self.contact)


# 新增订单
def add_object(order,money,buyer):
    db.session.add(order)
    db.session.add(money)
    db.session.add(buyer)
    db.session.commit()
    print("add %r " % order.__repr__)
    print("add %r " % money.__repr__)
    print("add %r " % buyer.__repr__)


def get_all_orders(order, money, buyer, page):
    order_list = []

    num = order.query.count()

    if num > 50:
        start = num - page * 50 + 1
        if start < 0:
            start = 1
        end = num - (page - 1) * 50
        # num = end - start + 1
    else:
        start = 1
        end = num

    len = range(end, start - 1, -1)  # 逆序
    for i in len:
        order_data = order.query.get(i)
        money_data = money.query.get(i)
        buyer_data = buyer.query.get(i)

        if order_data == None:
            continue

        data = {
            "orderId": order_data.id,
            "dateTime": str(order_data.dateTime),
            "productName": order_data.productName,
            "productType": order_data.productType.split('/'),
            "productDescription": eval(order_data.productDescription),
            "purchasePrice": money_data.purchasePrice,
            "soldPrice": money_data.soldPrice,
            "postPrice": money_data.postPrice,
            "profit": money_data.profit,
            "purchaser": buyer_data.purchaser,
            "contact": buyer_data.contact,
            "platform": order_data.platform,
        }
        if order_data.accessories != None:
            data['accessories'] = order_data.accessories.split('/')
        if order_data.note != '':
            data['note'] = order_data.note

        # 在server层转换json会在结果中多出很多\
        # data_json = json.dumps(data)
        order_list.append(data)

    back_data = {
        'orderList': order_list,
        'total': num
    }
    return back_data


def get_order(order_id):
    order = Order.query.get(order_id)
    money = Money.query.get(order_id)
    purchaser = Buyer.query.get(order_id)
    is_active = int.from_bytes(order.isActive, byteorder='big')

    if is_active:
        back_data = {
            'productType': order.productType.split('/'),
            'productName': order.productName,
            'withAccessories': int.from_bytes(order.withAccessories, byteorder='big'),
            'productDescription': order.productDescription,
            'platform': order.platform,
            'note': order.note,
            "money": {
                'purchasePrice': money.purchasePrice,
                'soldPrice': money.soldPrice,
                'postPrice': money.postPrice,
            },
            'purchaser': purchaser.purchaser,
            'contact': purchaser.contact
        }
        if back_data['withAccessories']:
            back_data['accessories'] = order.accessories.split('/')
        return back_data
    else:
        return 'failed'


def delete_order(order_id):
    order = Order.query.get(order_id)
    order.isActive = 0
    return 1

