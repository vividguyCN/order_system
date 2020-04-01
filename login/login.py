from flask import request, session, Response
import json
from login.database import User, query_object, add_object
from application import app
import logging


@app.route("/api/login", methods=["POST"])
def login():
    '''
    This is the Login API
    Call this api to login
    ---
    tags:
      - Login
    parameters:
      - name: username
        in: body
        type: string
        required: true
        description: username or email
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
        schema:
          $ref: "#/definitions/LoginJson"
      403:
        description: Login failed return code 403 and string
        schema:
             properties:
                msg:
                  type: string
                  example: 用户未注册或被封禁

    definitions:
        LoginJson:
          properties:
            uid:
              type: integer
              example: 1
    '''
    if request.method == "POST":
        # 设置session
        session.permanent = True  # 默认31天过期

        # 获取数据 json
        user_info = request.get_json()
        back_data = {
            'username': user_info.get('username'),
            'password': user_info.get('password')
        }

        # 数据库查询
        result = query_object(back_data['username'], back_data['password'], ' ', 'login')
        if result == '':
            result = query_object('', back_data['password'], back_data['username'], 'login')

        if result != '':
            # 对登录成功的用户，返回状态码和json
            # json使用字典
            uid = result.uid
            json_data = {
                "uid": str(uid)
            }
            # 添加session
            session['username'] = back_data['username']
            session['uid'] = json_data['uid']
            session['password'] = back_data['password']
            session['email'] = result.email

            app.logger.info('%s logged in successfully', back_data['username'])

            return json.dumps(json_data), 200
    # 登录失败 返回状态码
    app.logger.info('%s failed to login in ', back_data['username'])
    json_data = {
        "msg": "账户未注册或被封禁"
    }
    return json.dumps(json_data), 403


@app.route("/api/register", methods=["POST"])
def register():
    '''
    This is the Register API
    Call this api to register
    ---
    tags:
      - Register
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
        description: success return verified=true,failed return verified=false and reason
        schema:
           $ref: "#/definitions/RegisterJson"

    definitions:
        RegisterJson:
          properties:
            verified:
              type: boolean
              example: false
            reason:
              type: string
              example: 相同的用户名
    '''
    if request.method == "POST":
        # 获取数据
        user_info = request.get_json()
        back_data = {
            'username': user_info.get('username'),
            'password': user_info.get('password'),
            'email': user_info.get('email'),
        }
        back_json = {
            'verified': True,
            'reason': '成功'
        }

        # 数据库查询
        # 检查是否存在相同username,email
        result = query_object(back_data['username'], '', back_data['email'], 'register')
        print(result)
        if result == 1:
            back_json['reason'] = '用户名被占用'
            back_json['verified'] = False
            app.logger.info('%s register failed ,reason : %s', back_data['username'], back_json['reason'])
        elif result == 2:
            back_json['reason'] = '已存在的邮箱地址，请直接登录'
            back_json['verified'] = False
            app.logger.info('%s register failed ,reason : %s', back_data['username'], back_json['reason'])
        elif result == 3:
            # add new_account
            user = User()
            user.username = back_data['username']
            user.password = back_data['password']
            user.email = back_data['email']
            user.isActive = 1
            add_object(user)
            app.logger.info('%s register successfully ', back_data['username'])

    return json.dumps(back_json), 200


@app.route("/api/logout", methods=["POST"])
def logout():
    """
     This is the Logout API
    Call this api to logout
    ---
    tags:
      - Logout
    responses:
      200:
        description: logout success clear session
        schema:
          status:
            type: string
            example: success
    """
    session.clear()
    back_json = {
        "status": "success"
    }
    return json.dumps(back_json), 200
