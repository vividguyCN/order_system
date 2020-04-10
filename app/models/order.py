from app.common import db


class Order(db.Model):
    # order info
    __tablename__ = 'order_info'
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
        return '<Order id:%r name:%r sku:%r>' % (self.id,self.productName,self.productDescription)


class OrderMoney(db.Model):
    # order money
    _tablename_ = 'order_money'
    id = db.Column(db.Integer,primary_key=True)
    purchasePrice = db.Column(db.Integer, unique=True)
    soldPrice = db.Column(db.Integer, unique=True)
    postPrice = db.Column(db.Integer, unique=True)
    profit = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<Money id:%r profit%r>' % (self.id,self.profit)


class Buyer(db.Model):
    # purchaser info
    __tablename__ = 'order_purchaser'
    id = db.Column(db.Integer, primary_key=True)
    purchaser = db.Column(db.String(255),unique=True)
    contact = db.Column(db.String(255),unique=True)

    def __repr__(self):
        return '<Purchaser name:%r contact:%r>' % (self.purchaser,self.contact)
