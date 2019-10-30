from flask import request,jsonify,current_app
from . import api
from app.utils.response_code import RET
from app.utils.common import login_required,power_filter
from app.model import Attribute,db

@api.route("/attribute/add",methods=["POST"])
@login_required
@power_filter
def attributeAdd():
    '''
    新增属性
    :return:状态
    '''

    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="未接收到数据")

    name = res_dir.get("name")
    image = res_dir.get("image")
    intro = res_dir.get("intro")

    if not all ([name,image,intro]):
        return jsonify(code=RET.PARAMERR,msg="请填写完整")

    attribute = Attribute(name=name,image=image,intro=intro)

    try:
        db.session.add(attribute)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="属性名称已存在")

    return jsonify(code=RET.OK,msg="成功")

@api.route("/attribute/list")
def attributeList():
    '''
    获取属性列表
    参数：detail 0 或不传为下拉框， 1 为详情
    :return:list
    '''
    detail = request.args.get("detail")

    try:
        list = Attribute.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="查询失败")

    data = []
    if detail is None or detail is "0":
        for attribute in list:
            select = attribute.getSelect()
            data.append(select)
    else:
        for attribute in list:
            info = {
                "name":attribute.name,
                "id":attribute.id,
                "image":attribute.image,
                "intro":attribute.intro
            }
            data.append(info)

    return jsonify(code=RET.OK,data=data,msg="成功")

@api.route("/attribute/delete/<int:id>")
@login_required
@power_filter
def attributeDelete(id):
    '''
    删除属性
    :param id:
    :return:状态
    '''
    try:
        attribute = Attribute.query.get(id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="查找不到删除的数据")

    try:
        db.session.delete(attribute)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR, msg="当前属性已被角色使用")

    return jsonify(code=RET.OK,msg="删除成功")

@api.route("/attribute/update",methods=["POST"])
@login_required
@power_filter
def attributeUpdate():
    '''
    编辑属性
    :return:状态
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="未接收到数据")

    id = res_dir.get("id")
    name = res_dir.get("name")
    image = res_dir.get("image")
    intro = res_dir.get("intro")

    if not all([name,image,intro]):
        return jsonify(code=RET.PARAMERR,msg="参数不完整")

    try:
        Attribute.query.filter_by(id=id).update({"name":name,"image":image,"intro":intro})
        db.session.commit()
    except Exception as e :
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="修改失败")

    return jsonify(code=RET.OK,msg="修改成功")

@api.route("/attribute/detail/<int:id>")
def attributeDetail(id):
    '''
    属性详情
    :param id:
    :return:属性
    '''
    attribute = Attribute.query.get(id)

    if attribute is None:
        return jsonify(code=RET.DATAERR,msg="查找不到属性")

    role = []
    beast = []

    for i in attribute.role:
        info = {
            "id":i.id,
            "name":i.name,
            "head_portrait":i.head_portrait
        }
        role.append(info)

    for i in attribute.beast:
        info = {
            "id": i.id,
            "name": i.name,
            "head_portrait": i.head_portrait
        }
        beast.append(info)

    data = {
        "id":attribute.id,
        "name":attribute.name,
        "image":attribute.image,
        "intro":attribute.intro,
        "role":role,
        "beast":beast,
        "update_time":attribute.update_time
    }
    return jsonify(code=RET.OK,data=data,msg="成功")