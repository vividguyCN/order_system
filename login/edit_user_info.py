from flask import request, session
import json
from login.database import query_object,  edit_user
from application import app
import logging


@app.route("/api/editUserInfo", methods=["PUT"])
def edit_user_info():
    """
    This is the EditUserInfo API
    Call this api to Edit user information
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
            app.logger.info('%s change name to %s', session['username'],new_info['new_name'])

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
                app.logger.info('%s change password', session['username'])
            else:
                # 考虑优先级问题
                back_json['reason'] = '原密码输入错误'

    return json.dumps(back_json), 200


@app.route("/api/getUserInfo", methods=["GET"])
def get_UserInfo():
    """
    This is the GetUserInfo API
    Call this api to Get user information
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
        "email": session['email']
    }
    return json.dumps(back_json)

