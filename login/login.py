from flask import Flask, render_template, request
import json
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import and_


app = Flask(__name__)

# 配置数据库
DEBUG = True
SQLALCHEMY_ECHO = False
SECREET_KEY = os.urandom(24)
HOSTNAME = 'localhost'
PORT = '3306'
DATEBASE = 'login'
USERNAME = 'root'
PASDWORD = '123'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASDWORD,HOSTNAME,PORT,DATEBASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app, use_native_unicode='utf8')

class User(db.Model):
    __tablename__ = 'login'
    uid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255),unique=True)
    email = db.Column(db.String(255),unique=True)
    def __repr__(self):
        return '<User username:%r password: %r email:%r>' % (self.username,self.password,self.email)

def add_object(user):
    db.session.add(user)
    db.session.commit()
    print("add %r " % user.__repr__)


def query_object(user, u_name, u_psd):
    # result = user.query.filter(u_name == user.username).all()

    result = User.query.filter(and_(User.username == u_name, User.password == u_psd)).all()
    # result = User.query.all()
    # print(result)
    # print(result == [])
    # for item in result:
    #     print(item.username,item.password)
    # print('find %r' % user.__repr__)
    return result


# db.create_all()
# user = User()
# query_object('admin', '123456')


# 指定请求方式，如果不指定，则无法匹配到请求

@app.route("/", methods=("GET", "POST"))
def login():
    # GET请求
    if request.method == "GET":
        return render_template("login.html")
    # POST请求
    if request.method == "POST":

        # print(request.headers)
        # print()
        # print(request.json)
        # print()
        # print(request.data)
        # 获取数据并转化成字典
        user_info = request.form.to_dict()
        # 从数据库中读取
        back_data = {
            'username':user_info.get('username'),
            'password':user_info.get('password'),
            'email':user_info.get('email')
        }
        # print(back_data)
        user = User()
        result = query_object(user, back_data['username'], back_data['password'])
        # result_json = json.dumps(result, ensure_ascii=False)
        print(result)
        # if user_info.get("username") == "admin" and user_info.get("password") == '123456':
        if result != []:
            # 对登录成功的用户，返回状态码和cookie和josn
            # json使用字典

            return json.dumps(back_data), 200
    # print(request.form.to_dict())
    # args 获取地址栏的hash值
    # print(request.args.to_dict())
    return 'failed', 404

app.run(host="0.0.0.0", port=3000, debug=True)