from flask import request, session, Blueprint
import json
from app.models.users import User
from app.database.login import query_object, add_object, edit_user

user_api = Blueprint('user', __name__)


@user_api.route("/login", methods=["POST"])
def login():
    """
    使用这个api来让用户登录
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
    """
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
            session['username'] = result.username
            session['uid'] = result.uid
            session['password'] = result.password
            session['email'] = result.email
            session['permissions'] = result.permissions

            # app.logger.info('%s logged in successfully', back_data['username'])

            return json.dumps(json_data), 200
    # 登录失败 返回状态码
    # user_api.logger.info('%s failed to login in ', back_data['username'])
    json_data = {
        "msg": "账户未注册或被封禁"
    }
    return json.dumps(json_data), 403


@user_api.route("/register", methods=["POST"])
def register():
    """
    使用这个api来创建新的账户
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
    """
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
        if result == 1:
            back_json['reason'] = '用户名被占用'
            back_json['verified'] = False
            # user_api.logger.info('%s register failed ,reason : %s', back_data['username'], back_json['reason'])
        elif result == 2:
            back_json['reason'] = '已存在的邮箱地址，请直接登录'
            back_json['verified'] = False
            # user_api.logger.info('%s register failed ,reason : %s', back_data['username'], back_json['reason'])
        elif result == 3:
            # add new_account
            user = User()
            user.username = back_data['username']
            user.password = back_data['password']
            user.email = back_data['email']
            user.permissions = 2
            user.isActive = 1
            add_object(user)
            # user_api.logger.info('%s register successfully ', back_data['username'])

    return json.dumps(back_json), 200


@user_api.route("/logout", methods=["POST"])
def logout():
    """
    使用这个api来登出用户的账户,清理session
    ---
    tags:
      - Logout
    responses:
      200:
        description: logout success clear session
        schema:
             properties:
                status:
                  type: string
                  example: success
    """
    # user_api.logger.info('%s logout successfully.', session['username'])
    session.clear()
    back_json = {
        "status": "success"
    }
    return json.dumps(back_json), 200


@user_api.route("/editUserInfo", methods=["PUT"])
def edit_user_info():
    """
    使用这个api来修改用户的个人信息
    ---
    tags:
      - EditUserInformation
    put:
      parameters:
        - name: username
          in: body
          type: string
          required: true
          description: 新的用户名
          example: new_name
        - name: email
          in: body
          type: string
          required: true
          description: 新的邮箱
          example: new_email@email.com
        - name: changePassword
          in: body
          type: boolean
          required: true
          description: 是否修改密码
          example: 1
        - name: oldPassword
          in: body
          type: string
          description: 旧密码
          example: 123456
        - name: newPassword
          in: body
          type: string
          description: 新的密码
          example: 654321
    responses:
        200:
          description: post，修改成功
          schema:
            properties:
              status:
                type: string
                description: 修改状态
                example: success
        403:
          description: post， 修改失败
          schema:
            properties:
              status:
                type: string
                description: 修改状态
                example: failed
              reason:
                type: string
                description: 错误原因
                example: 用户名已被占用
    """
    if request.method == "PUT":
        # 获取数据 json
        data = request.get_json()
        back_json = dict()
        # 通过session 获取uid访问数据库
        new_info = {
            'new_name': data.get('username'),
            'new_email': data.get('email')
        }
        uid = int(session['uid'])

        # 查询可否修改
        if new_info['new_email'] == session['email'] and new_info['new_name'] == session['username']:
            result = 0
        elif new_info['new_name'] == session['username']:
            result = query_object('','',new_info['new_email'],'edit_info')
        elif new_info['new_email'] == session['email']:
            result = query_object(new_info['new_name'], '', '', 'edit_info')
        else:
            result = query_object(new_info['new_name'], '', new_info['new_email'], 'edit_info')

        back_json['status'] = 'failed'
        if result == 0:
            back_json['status'] = 'success'
        elif result == 1:
            back_json['reason'] = '用户名被占用'
        elif result == 2:
            back_json['reason'] = '邮箱已注册'
        elif result == 3:
            edit_user(uid, 1, new_info)
            back_json['status'] = 'success'
            session['username'] = new_info['new_name']
            session['email'] = new_info['new_email']
            # app.logger.info('%s change name to %s', session['username'],new_info['new_name'])

        # 如果用户申请修改密码
        if data.get('changePassword') == 1:
            # 检查密码
            old_password = data.get('oldPassword')
            psd = session['password']

            if psd == old_password:
                new_password = data.get('newPassword')
                new_info['new_psd'] = new_password
                edit_user(uid, 2, new_info)
                back_json['status'] = 'success'
                session['password'] = new_password
                # app.logger.info('%s change password', session['username'])
            else:
                # 考虑优先级问题
                # app.logger.info('%s change password failed', session['username'])
                back_json['reason'] = '原密码输入错误'

    return json.dumps(back_json), 200


@user_api.route("/getUserInfo", methods=["GET"])
def get_user_info():
    """
    使用这个api来获取用户的个人信息
    ---
    tags:
      - GetUserInformation
    parameters:
      - name: session
        in: head
        required: true
        description: session
    responses:
      200:
        description: 返回用户信息
        schema:
           $ref: "#/definitions/getUserInfo"
    definitions:
        getUserInfo:
          properties:
            username:
              type: string
              example: admin
            email:
              type: string
              example: admin@email.com
    """
    back_json = {
        "username": session['username'],
        "email": session['email'],
        "permissions": session['permissions']
    }
    return json.dumps(back_json)