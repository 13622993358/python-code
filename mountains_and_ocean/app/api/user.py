from . import api
from flask import request,jsonify,current_app
from app.utils.response_code import RET
from app.model import User,db
from app.utils.common import generate_token,login_required,verify_token
import re

@api.route("/register",methods=['POST'])
def register():
    '''
    注册用户
    :return:token
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code = RET.PARAMERR,msg = "请完整填写")

    phone = res_dir.get("phone")
    password = res_dir.get("password")
    name = res_dir.get("name")

    if not all([phone,password,name]):
        return jsonify(code = RET.PARAMERR,msg = "请完整填写")

    user = User(phone=phone,password=password,name=name)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code = RET.DATAERR,msg = "手机号已存在")

    token = generate_token(user.id)

    data = {
        "name":name,
        "phone":phone,
        "token":token,
    }
    return jsonify(code=RET.OK,msg="成功",data=data)

@api.route("/login",methods=["POST"])
def login():
    '''
    用户登录
    :return:token
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code = RET.PARAMERR,msg = "请填写手机号与密码")

    phone = res_dir.get("phone")
    password = res_dir.get("password")

    if not all([phone,password]):
        return jsonify(code=RET.PARAMERR, msg="请填写手机号或密码")

    if not re.match(r"1[23456789]\d{9}",phone):
        return jsonify(code=RET.PARAMERR,msg="手机号有误")

    try:
        user = User.query.filter_by(phone=phone).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="获取信息失败")

    if user is None or not user.check_password(password):
        return jsonify(code=RET.PARAMERR,msg="手机号或密码错误")

    token = generate_token(user.id)

    return jsonify(code=RET.OK,msg="成功",data=token)

@api.route("/user/detail")
@login_required
def userInfo():
    '''
    用户信息
    :return:
    '''
    token = request.headers["z-token"]
    user = verify_token(token)

    data = {
        "phone":user.phone,
        "name":user.name,
        "head_portrait":user.head_portrait,
        "intro":user.intro,
        "level":user.level
    }

    return jsonify(code=RET.OK,msg="成功",data=data)

@api.route("/user/update",methods=["POST"])
@login_required
def userUpdate():
    '''
    用户更新
    :return:状态
    '''

    res_dir = request.get_json()
    token = request.headers["z-token"]
    user = verify_token(token)
    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="无接收到参数")

    name = res_dir.get("name")
    head_portrait = res_dir.get("head_portrait")
    intro = res_dir.get("intro")

    if name is '' or name is None:
        return jsonify(code=RET.PARAMERR,msg="请填写昵称")

    try:
        User.query.filter_by(id=user.id).update({"name":name,"head_portrait":head_portrait,"intro":intro})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="修改失败")

    return jsonify(code=RET.OK,msg="成功")


