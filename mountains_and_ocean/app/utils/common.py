from flask import request,jsonify,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.utils.const import tokenExpires
from app.model import User
from app.utils.response_code import RET
import functools

#生成token
def generate_token(api_user):
    #密钥 = 私有密钥+有效期+用户id
    s = Serializer(current_app.config["SECRET_KEY"],expires_in=tokenExpires)
    token = s.dumps({"id":api_user}).decode("ascii")
    return token

#校验token
def verify_token(token):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        data = s.loads(token)
    except Exception as e:
        current_app.logger.error(e)
        return None
    user = User.query.get(data["id"])
    return user

#必须携带token的装饰器
def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        try:
            token = request.headers["z-token"]
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code = RET.SESSIONERR,msg = '缺少参数token')

        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code = RET.SESSIONERR,msg = "登录已过期")

        return view_func(*args,**kwargs)

    return verify_token

#校验权限
def power_filter(view_func):
    @functools.wraps(view_func)
    def filterLevel(*args,**kwargs):
        try:
            token = request.headers["z-token"]
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code = RET.SESSIONERR,msg = "缺少参数token")

        user = verify_token(token)

        level = user.level

        if int(level) < 5 :
            return jsonify(code = RET.ROLEERR, msg = "权限不足")

        return view_func(*args,**kwargs)

    return filterLevel