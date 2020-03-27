from flask_sqlalchemy import SQLAlchemy
from application import app
from config import DB_URI

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app,use_native_unicode='utf8')

# 数据库类型
class Order(db.Model):
    # order info
    __tablename__ = 'info'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    time = db.Column(db.DateTime, unique=True)
    type = db.Column(db.String(255),unique=True)
    name = db.Column(db.String(255),unique=True)
    sku = db.Column(db.String(255),unique=True)
    withAccessories = db.Column(db.Boolean, unique=True)
    accessories = db.Column(db.String(255),unique=True)
    platform = db.Column(db.String(255),unique=True)
    remark = db.Column(db.String(255),unique=True)
    isActive = db.Column(db.Boolean,unique=True)
    def __repr__(self):
        # 只返回订单id
        return '<Order id:%r name:%r sku:%r>' % (self.id,self.name,self.sku)

class Money(db.Model):
    # order money
    _tablename_ = 'money'
    id = db.Column(db.Integer,primary_key=True)
    income = db.Column(db.Integer, unique=True)
    sold = db.Column(db.Integer, unique=True)
    post = db.Column(db.Integer, unique=True)
    profit = db.Column(db.Integer, unique=True)
    def __repr__(self):
        return '<Order id:%r profit%r>' % (self.id,self.profit)


class Buyer(db.Model):
    # purchaser info
    __tablename__ = 'purchaser'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique=True)
    contact = db.Column(db.String(255),unique=True)
    def __repr__(self):
        return '<Purchaser name:%r contact:%r>' % (self.name,self.contact)


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
    # page1 : 1~50,page2 : 51~100
    start = (page - 1) * 50 + 1
    len = range(start, order.query.count() + 1)
    for i in len:
        order_data = order.query.get(i)
        money_data = money.query.get(i)
        buyer_data = buyer.query.get(i)
        if(order_data == None ):
            continue

        data = {
            "datetime": str(order_data.time),
            "name": order_data.name,
            "type": order_data.type,
            "income": money_data.income,
            "sold": money_data.sold,
            "post": money_data.post,
            "profit": money_data.profit,
            "purchaser": buyer_data.name,
            "contact": buyer_data.contact,
            "platform": order_data.platform
        }
        # 在server层转换json会在结果中多出很多\
        # data_json = json.dumps(data)
        order_list.append(data)

    return order_list

# TODO 查找订单

