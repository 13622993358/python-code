from . import api
from flask import request,jsonify,current_app
from app.model import Group,db
from app.utils.response_code import RET
from app.utils.common import login_required,power_filter

@api.route("/group/add",methods=["POST"])
@login_required
@power_filter
def groupAdd():
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR, msg="未接收到数据")

    name = res_dir.get("name")
    image = res_dir.get("image")
    site = res_dir.get("site")
    intro = res_dir.get("intro")
    level = res_dir.get("level")

    if not all([name, image, site, level]):
        return jsonify(code=RET.PARAMERR, msg="参数不完整")

    group = Group(name=name,image=image,site=site,intro=intro,level=level)

    try:
        db.session.add(group)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code=RET.DATAERR, msg="创建失败")

    return jsonify(code=RET.OK, msg="创建成功")

@api.route("/group/delete/<int:id>")
@login_required
@power_filter
def groupDelete(id):
    group = Group.query.get(id)

    if group is None:
        return jsonify(code=RET.DATAERR,msg="未查找到要删除的数据")

    try:
        db.session.delete(group)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR, msg="删除失败")

    return jsonify(code=RET.OK, msg="删除成功")

@api.route("/group/update",methods=["POST"])
@login_required
@power_filter
def groupUpdate():
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR, msg="未接收到数据")

    id = res_dir.get("id")
    name = res_dir.get("name")
    image = res_dir.get("image")
    site = res_dir.get("site")
    intro = res_dir.get("intro")
    level = res_dir.get("level")

    if not all([id, name, image, site, level]):
        return jsonify(code=RET.PARAMERR, msg="参数不完整")

    try:
        Group.query.filter_by(id=id).update({"name":name,"image":image,"site":site,"intro":intro,"level":level})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="修改失败")

    return jsonify(code=RET.OK, msg="修改成功")

@api.route("/group/list")
def groupList():
    isSeletc = request.args.get("isSelect")
    data = []

    if isSeletc is not None and isSeletc == "0":
        # 下拉框模式
        groupList = Group.query.all()
        for group in groupList:
            select = Group.getSelect(group)
            data.append(select)
    else:
        # 列表展示模式
        # 筛选数据
        name = request.args.get("name")
        site = request.args.get("site")
        level = request.args.get("level")

        filterList = []

        if name is not None:
            filterList.append(Group.name.like("%"+name+"%"))
        if site is not None:
            filterList.append(Group.site == site)
        if level is not None:
            filterList.append(Group.level == level)

        groupList = Group.query.filter(*filterList).all()

        for group in groupList:
            info = {
                "id": group.id,
                "name": group.name,
                "level": group.level,
                "image": group.image
            }
            data.append(info)

    return jsonify(code=RET.OK, msg="成功", data=data)

@api.route("/group/detail/<int:id>")
def groupDetail(id):
    group = Group.query.get(id)

    if group is None:
        return jsonify(code=RET.DATAERR, msg="未查找到数据")

    getRoleList = group.role
    roleList = []
    for role in getRoleList:
        info = {
            "id": role.id,
            "name": role.name,
            "head_portrait": role.head_portrait
        }
        roleList.append(info)

    data = {
        "id": group.id,
        "name": group.name,
        "image": group.image,
        "intro": group.intro,
        "level": group.level,
        "role": roleList
    }

    return jsonify(code=RET.OK, msg="成功", data=data)