from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,or_
from app import app
from config import DB_URI


app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app,use_native_unicode='utf8')

# 数据库类型
class User(db.Model):
    __tablename__ = 'login'
    uid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255),unique=True)
    email = db.Column(db.String(255),unique=True)
    def __repr__(self):
        return '<User username:%r password: %r email:%r>' % (self.username,self.password,self.email)

# 增加
def add_object(user):
    db.session.add(user)
    db.session.commit()
    print("add %r " % user.__repr__)

# username 和 psd 查找
def query_object(u_name, u_psd, u_email, type):
    if(type == 'login'):
        print('login')
        result = User.query.filter(and_(User.username == u_name, User.password == u_psd)).all()
    elif(type == 'register'):
        print('register')
        result = User.query.filter(or_(User.username == u_name, User.email == u_email)).all()
        if(result != []):
            # 这个地方很奇怪，为什么username不用query？
            # if User.username == u_name and User.email == u_email:
            if User.query.filter(and_(User.username == u_name, User.email == u_email)).all():
                return 3  # both same
            elif User.query.filter(User.email == u_email).all():
                return 2  # same email
            elif User.query.filter(User.username == u_name).all():
                return 1  # same username
        else:
            return 4  # register success
    print(result)
    # print('find %r' % user.__repr__)
    return result


# db.create_all()