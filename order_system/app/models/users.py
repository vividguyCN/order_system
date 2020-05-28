from app.common import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# 根据userId 创建token
def create_token(user_id):
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    token = s.dumps({"id": user_id}).decode("ascii")
    return token


def verify_token(token):
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        return None
    # 拿到转换后的数据，根据模型类去数据库查询用户信息
    user = User.query.get(data["id"])
    # 返回token中储存的用户
    return user


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    isActive = db.Column(db.Integer, unique=True)  # 记录用户封禁状态
    role = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<User uid:%r username:%r password: %r email:%r>' % (self.uid, self.username,self.password,self.email)