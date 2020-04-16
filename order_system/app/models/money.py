from app.common import db


class MoneyDetail(db.Model):
    # money detail
    _tablename_ = 'money_detail'
    id = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.DateTime, unique=True)
    typeId = db.Column(db.Integer, unique=True)
    # 订单为0,库存为1
    moneyType = db.Column(db.Integer, unique=True)
    productName = db.Column(db.String, unique=True)
    productType = db.Column(db.String, unique=True)
    money = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<Money id:%r type: %r money:%r>' % (self.id, self.moneyType, self.money)
