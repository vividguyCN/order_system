from flask import request
import json
from database import User,query_object, add_object
from app import app
from flasgger import Swagger, swag_from

Swagger(app)

@app.route("/api/login", methods=["POST"])
def login():
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
        description: Login success
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
            back_data['reason'] = 'same username'
        elif result == 2:
            back_data['reason'] = 'same email'
        elif result == 3:
            back_data['reason'] = 'both same'
        elif(result == 4):
            # add new_account
            user = User()
            user.username = back_data['username']
            user.password = back_data['password']
            user.email = back_data['email']
            add_object(user)

    return json.dumps(back_data), 200

app.run(host="0.0.0.0", port=3000, debug=True)