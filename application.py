from flask import Flask
from flasgger import Swagger
from datetime import timedelta
import os


app = Flask(__name__)
Swagger(app)

app.config['SECRET_KEY'] = os.urandom(24)  # 使用一组随机数对session进行加密
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # 修改session 过期时间 --> session.permanent = True