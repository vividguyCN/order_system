from flask import Flask
from flasgger import Swagger
from datetime import timedelta
import os


app = Flask(__name__)
Swagger(app)

app.config['SECRET_KEY'] = os.urandom(24)  # 使用一组随机数对session进行加密
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # 修改session 过期时间 --> session.permanent = True
# 查询时显示原始的sql语句
app.config['SQLALCHEMY_ECHO'] = False
# 设置每次请求结束后会自动提交数据库的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
