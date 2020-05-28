from flask import request, session, Blueprint, current_app, make_response
import json
from app.models.users import User, create_token, verify_token
from app.database.login import query_object, add_object, edit_user

user_api = Blueprint('user', __name__)


@user_api.route("/login", methods=["POST"])
def login():
    if request.method == "POST":

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

            current_app.logger.info('%s logged in successfully', back_data['username'])
            # 根据uid创建token
            token = create_token(uid)

            json_data = {
                "status": 'success'
            }
            rsp = make_response(json.dumps(json_data))
            rsp.headers['Authorization'] = token

            return rsp, 200
    # 登录失败 返回状态码
    current_app.logger.info('%s failed to login in ', back_data['username'])
    json_data = {
        "msg": "账户未注册或被封禁"
    }
    return json.dumps(json_data), 403


@user_api.route("/register", methods=["POST"])
def register():
    # 获取token
    token = request.headers.get('token')
    # 注册账号信息
    user_info = request.get_json()
    back_data = {
        'username': user_info.get('username'),
        'password': user_info.get('password'),
        'email': user_info.get('email'),
        'role': user_info.get('role')
    }
    # 返回状态信息
    back_json = {
        'verified': True,
        'reason': '成功'
    }
    # 判断用户是否有注册权限
    # 1-admin 可以创建账号
    admin = verify_token(token)
    if admin == None:
        return 'Bad Request', 400
    if admin.role == 1:
        # 数据库查询
        # 检查是否存在相同username,email
        result = query_object(back_data['username'], '', back_data['email'], 'register')
        if result == 1:
            back_json['reason'] = '用户名被占用'
            back_json['verified'] = False
            current_app.logger.info('%s register failed ,reason : %s', back_data['username'], back_json['reason'])
        elif result == 2:
            back_json['reason'] = '已存在的邮箱地址，请直接登录'
            back_json['verified'] = False
            current_app.logger.info('%s register failed ,reason : %s', back_data['username'], back_json['reason'])
        elif result == 3:
            # add new_account
            user = User()
            user.username = back_data['username']
            user.password = back_data['password']
            user.email = back_data['email']
            user.role = back_data['role']
            user.isActive = 1
            add_object(user)
            current_app.logger.info('%s register successfully ', back_data['username'])
    else:
        back_json = {
            'status': False,
            'reason': '你无权这么做'
        }

    return json.dumps(back_json), 200


@user_api.route("/logout", methods=["POST"])
def logout():
    current_app.logger.info('%s logout successfully.', session['username'])
    # 清除token
    # logout 成功
    back_json = {
        "status": "success"
    }
    return json.dumps(back_json), 200


@user_api.route("/editUserInfo", methods=["PUT"])
def edit_user_info():
    if request.method == "PUT":
        # 获取token
        token = request.headers.get('token')
        # 获取变更数据
        data = request.get_json()
        back_json = dict()
        new_info = {
            'new_name': data.get('username'),
            'new_email': data.get('email'),
        }
        user = verify_token(token)
        if user == None:
            return 'Bad Request', 400

        # 查询可否修改
        if new_info['new_email'] == user.email and new_info['new_name'] == user.username:
            result = 0
        elif new_info['new_name'] == user.username:
            result = query_object('', '', new_info['new_email'], 'edit_info')
        elif new_info['new_email'] == user.email:
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
        # 可以修改
        elif result == 3:
            edit_user(user.uid, 1, new_info)
            back_json['status'] = 'success'
            current_app.logger.info('%s change name to %s', user.username, new_info['new_name'])

        # 如果用户申请修改密码
        if data.get('changePassword') == 1:
            # 检查密码
            old_password = data.get('oldPassword')
            psd = user.password

            if psd == old_password:
                new_password = data.get('newPassword')
                new_info['new_psd'] = new_password
                edit_user(user.uid, 2, new_info)
                back_json['status'] = 'success'
                current_app.logger.info('%s change password', user.username)
            else:
                # 考虑优先级问题
                current_app.logger.info('%s change password failed', user.username)
                back_json['reason'] = '原密码输入错误'

    return json.dumps(back_json), 200


@user_api.route("/getUserInfo", methods=["GET"])
def get_user_info():
    token = request.headers.get('token')
    user = verify_token(token)
    try:
        back_json = {
            "username": user.username,
            "email": user.email,
            "role": user.rorle
        }
    except:
        return 'Bad Request', 400

    return json.dumps(back_json)
