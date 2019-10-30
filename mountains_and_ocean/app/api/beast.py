from . import api
from app.utils.common import login_required,power_filter
from app.model import Beast,db
from app.utils.response_code import RET
from flask import request,jsonify,current_app

@api.route("/beast/add",methods=['POST'])
@login_required
@power_filter
def beastAdd():
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="未接收到参数")

    name = res_dir.get("name")
    head_portrait = res_dir.get("head_portrait")
    attribute = res_dir.get("attribute")
    site = res_dir.get("site")
    intro = res_dir.get("intro")
    image_list = res_dir.get("image_list")

    if not all ([name,head_portrait,attribute,site]):
        return jsonify(code=RET.PARAMERR,msg="参数不完整")

    imageStr = ""
    if len(image_list) > 0:
        imageStr = ",".join(image_list)

    beast = Beast(name=name,head_portrait=head_portrait,attribute=attribute,site=site,intro=intro,image_list=imageStr)

    try:
        db.session.add(beast)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="添加失败")

    return jsonify(code=RET.OK, msg="添加成功")

@api.route("/beast/delete/<int:id>")
@login_required
@power_filter
def beastDelete(id):
    beast = Beast.query.get(id)
    if beast is None:
        return jsonify(code=RET.DATAERR,msg="查找不到要删除的信息")

    try:
        db.session.delete(beast)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="删除失败")

    return jsonify(code=RET.OK, msg="删除成功")

@api.route("/beast/update",methods=["POST"])
@login_required
@power_filter
def beastUpdate():
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="未接收到参数")

    id = res_dir.get("id")
    name = res_dir.get("name")
    head_portrait = res_dir.get("head_portrait")
    attribute = res_dir.get("attribute")
    site = res_dir.get("site")
    intro = res_dir.get("intro")
    image_list = res_dir.get("image_list")

    if not all ([id,name,head_portrait,attribute,site]):
        return jsonify(code=RET.PARAMERR, msg="参数不完整")

    imgArr = ""
    if len(image_list) > 0:
        imgArr = ",".join(image_list)

    try:
        Beast.query.filter_by(id=id).update({"name":name,"head_portrait":head_portrait,"attribute":attribute,"site":site,"intro":intro,"image_list":imgArr})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR, msg="修改失败")

    return jsonify(code=RET.OK, msg="修改成功")

@api.route("/beast/list")
def beastList():
    pass

@api.route("/beast/detail/<int:id>")
def beastDetail(id):
    beast = Beast.query.get(id)

    if beast is None:
        return jsonify(code=RET.DATAERR,msg="信息不存在")

    #属性
    attribute = Beast.getAttr(id)
    #地区
    site = Beast.getSite(id)

    data = {
        "id":beast.id,
        "name":beast.name,
        "head_portrait":beast.head_portrait,
        "site":site,
        "intro":beast.intro,
        "image_list":beast.image_list.split(","),
        "attribute":attribute,
        "update_time": beast.update_time
    }

    return jsonify(code=RET.OK,msg="成功",data=data)