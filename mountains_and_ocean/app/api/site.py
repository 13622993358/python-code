from . import api
from flask import request,jsonify,current_app
from app.utils.common import login_required,power_filter
from app.utils.response_code import RET
from app.model import Site,db

@api.route("/site/add",methods=["POST"])
@login_required
@power_filter
def siteAdd():
    '''
    新增区域
    :return:状态
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="未接收到数据")

    name = res_dir.get("name")
    image = res_dir.get("image")
    intro = res_dir.get("intro")

    if not all ([name,image,intro]):
        return jsonify(code=RET.PARAMERR,msg="参数不完整")

    site = Site(name=name,image=image,intro=intro)

    try:
        db.session.add(site)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="保存失败,名称已存在")

    return jsonify(code=RET.OK,msg="成功")

@api.route("/site/delete/<int:id>")
@login_required
@power_filter
def siteDelete(id):
    '''
    删除区域
    :param id:
    :return:状态
    '''
    site = Site.query.get(id)
    if site is None:
        return jsonify(code=RET.DATAERR,msg="查找不到要删除的数据")

    try:
        db.session.delete(site)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="删除失败")

    return jsonify(code=RET.OK,msg="删除成功")


@api.route("/site/list")
def siteList():
    '''
    区域列表
    :param detail=0 或不传为下拉框模式
    :return: 
    '''
    detail = request.args.get("detail")
    name = request.args.get("name")

    try:
        if name is not None and name is not "":
            list = Site.query.filter(Site.name.like("%"+name+"%")).all()
        else:
            list = Site.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="查询数据有误")

    data = []
    if detail is None or detail is "0":
        for i in list:
            select = i.getSelect()
            data.append(select)
    else:
        for i in list:
            info = {
                "id":i.id,
                "name":i.name,
                "image":i.image,
                "intro":i.intro
            }
            data.append(info)
    return jsonify(code=RET.OK,msg="成功",data=data)

@api.route("/site/detail/<int:id>")
def siteDetail(id):
    '''
    区域详情
    :param id:
    :return:data
    '''
    site = Site.query.get(id)
    if site is None:
        return jsonify(code=RET.DATAERR,msg="查找不到数据")

    role = []
    beast = []

    for i in site.role:
        info = {
            "id":i.id,
            "name":i.name,
            "head_portrait":i.head_portrait
        }
        role.append(info)

    for i in site.beast:
        info = {
            "id": i.id,
            "name": i.name,
            "head_portrait":i.head_portrait
        }
        beast.append(info)

    data = {
        "id":site.id,
        "name":site.name,
        "image":site.image,
        "intro":site.intro,
        "role":role,
        "beast":beast,
        "update_time":site.update_time
    }

    return jsonify(code=RET.OK,msg="成功",data=data)

@api.route("/site/update",methods=["POST"])
@login_required
@power_filter
def siteUpdate():
    '''
    区域信息更新
    :return: 状态
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR, msg="未接收到数据")

    id = res_dir.get("id")
    name = res_dir.get("name")
    image = res_dir.get("image")
    intro = res_dir.get("intro")

    if not all([id,name,image,intro]):
        return jsonify(code=RET.PARAMERR,msg="参数不完整")

    try:
        Site.query.filter_by(id=id).update({"name":name,"image":image,"intro":intro})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code=RET.DATAERR,msg="修改失败")

    return jsonify(code=RET.OK,msg="修改成功")



