from sqlalchemy import and_, or_
from app.models.users import User
from app.common import db


# 增加
def add_object(user):
    db.session.add(user)
    db.session.commit()
    print("add %r " % user.__repr__)


# username 和 psd 查找
def query_object(u_name, u_psd, u_email, flag):
    if flag == 'login':
        # login success return uid
        # 检查用户名 还是邮箱登录
        if u_name != '':
            result = User.query.filter(and_(User.username == u_name, User.password == u_psd)).first()
        elif u_email != '':
            result = User.query.filter(and_(User.email == u_email, User.password == u_psd)).first()

        if result != None and int.from_bytes(result.isActive, byteorder='big') == 1:
            # 查询有结果并且允许登录 返回uid
            return result
        else:
            return ''  # login failed
    elif flag == 'register' or 'edit_info':
        # 注册或者修改用户信息
        # print('register')
        result = User.query.filter(or_(User.username == u_name, User.email == u_email)).all()
        if result != []:
            if User.query.filter(User.email == u_email).all():
                return 2  # same email
            elif User.query.filter(User.username == u_name).all():
                return 1  # same username
        else:
            return 3  # register success


def edit_user(uid, change, new_info):
    # 修改用户名和邮箱
    new_name = new_info['new_name']
    new_email = new_info['new_email']
    user = User.query.get(uid)
    user.username = new_name
    user.email = new_email
    if change == 2:
        # 修改密码
        new_psd = new_info['new_psd']
        user.password = new_psd
    # update database
    db.session.commit()

    return 1
