from . import api
from app.model import Role,db
from app.utils.common import login_required,power_filter
from app.utils.response_code import RET
from flask import request,jsonify,current_app

@api.route("/role/add",methods=["POST"])
@login_required
@power_filter
def roleAdd():
    '''
    新增角色
    :return:状态
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="未接收到参数")
    name = res_dir.get("name")
    head_portrait = res_dir.get("head_portrait")
    gender = res_dir.get("gender")
    age = res_dir.get("age")
    attribute = res_dir.get("attribute")
    site = res_dir.get("site")
    intro = res_dir.get("intro")
    image_list = res_dir.get("image_list")

    if not all([name,head_portrait,gender,attribute,site]):
        return jsonify(code=RET.PARAMERR,msg="缺少参数")

    imgStr = ''
    if len(image_list) > 0:
        imgStr = ",".join(image_list)

    role = Role(name=name,head_portrait=head_portrait,gender=gender,age=age,attribute=attribute,site=site,intro=intro,image_list=imgStr)

    try:
        db.session.add(role)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="添加失败")

    return jsonify(code=RET.OK,msg="添加成功")

@api.route("/role/delete/<int:id>")
@login_required
@power_filter
def roleDelete(id):
   '''
   删除角色
   :param id:
   :return: 状态
   '''
   role = Role.query.get(id)

   if role is None:
       return jsonify(code=RET.DATAERR,msg="查找不到要删除的角色")

   try:
       db.session.delete(role)
       db.session.commit()
   except Exception as e:
       db.session.rollback()
       current_app.logger.error(e)
       return jsonify(code=RET.DATAERR,msg="删除角色失败")

   return jsonify(code=RET.OK,msg="删除成功")

@api.route("/role/list")
def roleList():
    '''
    角色列表
    :return:
    '''
    name = request.args.get("name")
    gender = request.args.get("gender")
    attribute = request.args.get("attribute")
    site = request.args.get("site")

    filterList = []

    if name is not None and name is not '':
        filterList.append(Role.name.like('%'+name+'%'))
    if gender is not None and gender is not '':
        filterList.append(Role.gender == gender)
    if attribute is not None and attribute is not '':
        filterList.append(Role.attribute == attribute)
    if site is not None and site is not '':
        filterList.append(Role.site == site)

    role = Role.query.filter(*filterList).all()

    data = []
    for i in role:
        info = {
            "id":i.id,
            "name":i.name,
            "attribute":i.attribute,
            "head_portrait":i.head_portrait
        }
        data.append(info)

    return jsonify(code=RET.OK,msg="成功",data=data)

@api.route("/role/detail/<int:id>")
def roleDetail(id):
    '''
    角色详情
    :param id:
    :return:
    '''
    role = Role.query.get(id)
    if role is None:
        return jsonify(code=RET.DATAERR,msg="未查找到数据")

    #角色属性
    attribute = Role.getAttr(id)
    #角色地区
    site = Role.getSite(id)

    data = {
        "id":role.id,
        "name":role.name,
        "head_portrait":role.head_portrait,
        "gender":role.gender,
        "age":role.age,
        "site":site,
        "intro":role.intro,
        "image_list":role.image_list.split(","),
        "attribute":attribute,
        "update_time": site.update_time
    }

    return jsonify(code=RET.OK,data=data)

@api.route("/role/update",methods=["POST"])
@login_required
@power_filter
def roleUpdate():
    '''
    角色修改
    :return:状态
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="未接收到参数")

    id = res_dir.get("id")
    name = res_dir.get("name")
    head_portrait = res_dir.get("head_portrait")
    gender = res_dir.get("gender")
    age = res_dir.get("age")
    attribute = res_dir.get("attribute")
    site = res_dir.get("site")
    intro = res_dir.get("intro")
    image_list = res_dir.get("image_list")

    if not all([id,name,head_portrait,gender,age,site]):
        return jsonify(code=RET.PARAMERR,msg="缺少参数")

    # 图片列表转数组
    imgStr = ''
    if len(image_list) > 0:
        imgStr = ",".join(image_list)

    try:
        Role.query.filter_by(id=id).update({"id":id,"name":name,"head_portrait":head_portrait,"gender":gender,"age":age,"attribute":attribute,"site":site,"intro":intro,"image_list":imgStr})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="修改失败")

    return jsonify(code=RET.OK,msg="修改成功")