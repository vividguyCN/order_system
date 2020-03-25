from flask import request
import json
from database import User,query_object, add_object
from app import app
from flasgger import Swagger, swag_from
import logging

Swagger(app)

@app.route("/api/login", methods=["POST"])
def login():
    # TODO add more responses description
    '''
    This is the Login API
    Call this api to login
    ---
    tags:
      - Login API
    parameters:
      - name: username
        in: body
        type: string
        required: true
        description: username
        example: admin
      - name: password
        in: body
        type: string
        required: true
        description: password
        example: 123456
    responses:
      200:
        description: return uid
        content:
            application/json:
            schema:
                type: object
                properties:
                    uid:
                        type: integer
                        description: user id
      403:
        description: Login failed
    '''
    # GET请求 之后去掉
    # if request.method == "GET":
    #     return render_template("login.html")
    # POST请求
    if request.method == "POST":
        # 获取数据 json
        # user_info = json.loads(request.form.get('data'))
        user_info = request.get_json()
        back_data = {
            'username': user_info.get('username'),
            'password': user_info.get('password')
        }
        # 数据库查询
        # TODO 查询成功直接返回uid的值
        result = query_object(back_data['username'], back_data['password'], ' ', 'login')
        # print(result[0])
        # print(json_data)
        if result != []:
            # 对登录成功的用户，返回状态码和json
            # json使用字典
            json_data = {
                "uid": str(result[0])
            }
            app.logger.info('%s logged in successfully',back_data['username'])
            return json.dumps(json_data), 200
    # print(request.form.to_dict())
    # 登录失败 返回状态码
    # TODO 可以改成abort
    app.logger.info('%S failed to login in ', back_data['username'])
    return 'failed', 403

@app.route("/api/register", methods=["POST"])
def register():
    '''
    This is the Register API
    Call this api to register
    ---
    tags:
      - Register API
    parameters:
      - name: username
        in: body
        type: string
        required: true
        description: username
        example: user
      - name: password
        in: body
        type: string
        required: true
        description: password
        example: 123456
      - name: email
        in: body
        type: string
        required: true
        description: email
        example: example@email.com
    responses:
      200:
        description: Returns specific failure information
    '''
    # GET请求
    # if request.method == "GET":
    #     return render_template("register.html")
    # POST请求
    if request.method == "POST":
        # 获取数据
        # user_info = json.loads(request.form.get('data'))
        user_info = request.get_json()
        back_data = {
            'username':user_info.get('username'),
            'password':user_info.get('password'),
            'email':user_info.get('email'),
            'reason':'register success'
        }

        # 数据库查询
        # 检查是否存在相同username,email
        result = query_object(back_data['username'], '', back_data['email'], 'register')
        print(result)
        if result == 1:
            back_data['reason'] = '用户名被占用'
        elif result == 2:
            back_data['reason'] = '已存在的邮箱地址，请直接登录'
        elif(result == 3):
            # add new_account
            user = User()
            user.username = back_data['username']
            user.password = back_data['password']
            user.email = back_data['email']
            add_object(user)

    return json.dumps(back_data), 200

app.run(host="0.0.0.0", port=3000, debug=True)