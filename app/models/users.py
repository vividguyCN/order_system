from app.common import db


class User(db.Model):
    __tablename__ = 'login'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    isActive = db.Column(db.Integer, unique=True)  # 记录用户封禁状态
    permissions = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<User uid:%r username:%r password: %r email:%r>' % (self.uid, self.username,self.password,self.email)