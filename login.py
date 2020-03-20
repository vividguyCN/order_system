from flask import render_template, request
import json
from database import User,query_object, add_object
from app import app


@app.route("/", methods=["GET", "POST"])
def login():
    # GET请求
    if request.method == "GET":
        return render_template("login.html")
    # POST请求
    if request.method == "POST":
        # 获取数据 json
        user_info = request.form.to_dict()
        back_data = {
            'username':user_info.get('username'),
            'password':user_info.get('password'),
            'email':user_info.get('email')
        }
        # 数据库查询

        result = query_object(back_data['username'], back_data['password'], ' ', 'login')
        print(result)
        if result != []:
            # 对登录成功的用户，返回状态码和json
            # json使用字典
            return json.dumps(back_data), 200
    # print(request.form.to_dict())
    # 登录失败 返回状态码
    return 'failed', 403

@app.route("/register", methods=("GET", "POST"))
def register():
    # GET请求
    if request.method == "GET":
        return render_template("register.html")
    # POST请求
    if request.method == "POST":
        # 获取数据
        user_info = request.form.to_dict()
        back_data = {
            'username':user_info.get('username'),
            'password':user_info.get('password'),
            'email':user_info.get('email')
        }
        # 数据库查询
        user = User()
        # 检查是否存在相同username,email
        result = query_object(back_data['username'], '', back_data['email'], 'register')
        if(result == []):
            # add new_account
            user.username = back_data['username']
            user.password = back_data['password']
            user.email = back_data['email']
            add_object(user)

            return json.dumps(back_data), 200
    # print(request.form.to_dict())
    # register失败 返回 josn （详细报错信息）
    return 'failed',200

app.run(host="0.0.0.0", port=3000, debug=True)