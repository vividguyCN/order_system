from app.common import db


class Stock(db.Model):
    # stock info
    __tablename__ = 'stock_info'
    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.Integer, unique=True)
    dateTime = db.Column(db.DateTime, unique=True)
    productType = db.Column(db.String(255),unique=True)
    productName = db.Column(db.String(255),unique=True)
    productDescription = db.Column(db.String(255),unique=True)
    platform = db.Column(db.String(255),unique=True)
    note = db.Column(db.String(255),unique=True)
    isSold = db.Column(db.Integer,unique=True)

    def __repr__(self):
        return '<Stock id:%r name:%r sku:%r>' % (self.id, self.productName, self.productDescription)


class StockMoney(db.Model):
    # stock money
    _tablename_ = 'stock_money'
    id = db.Column(db.Integer,primary_key=True)
    price = db.Column(db.Integer, unique=True)
    num = db.Column(db.Integer, unique=True)
    total = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<Money id:%r price:%r num:%r>' % (self.id, self.price, self.num)


class Creator(db.Model):
    # creator info
    __tablename__ = 'stock_creator'
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(255),unique=True)
    contact = db.Column(db.String(255),unique=True)

    def __repr__(self):
        return '<Creator name:%r contact:%r>' % (self.creator, self.contact)
