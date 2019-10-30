from . import  api
from app.model import College,db
from app.utils.common import login_required,power_filter
from app.utils.response_code import RET
from flask import request,jsonify,current_app

@api.route("/college/add",methods=["POST"])
@login_required
@power_filter
def collegeAdd():
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="未接收到数据")

    name = res_dir.get("name")
    image = res_dir.get("image")
    site = res_dir.get("site")
    intro = res_dir.get("intro")
    level = res_dir.get("level")

    if not all([name,image,site,level]):
        return jsonify(code=RET.PARAMERR,msg="参数不完整")

    collete = College(name=name,image=image,site=site,intro=intro,level=level)

    try:
        db.session.add(collete)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code=RET.DATAERR,msg="创建失败")

    return jsonify(code=RET.OK,msg="创建成功")

@api.route("/collete/delete/<int:id>")
@login_required
@power_filter
def colleteDelete(id):
    collete = College.query.get(id)

    if collete is None:
        return jsonify(code=RET.DATAERR,msg="未查找到要删除的数据")

    try:
        db.session.delete(collete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="删除失败")

    return jsonify(code=RET.OK,msg="删除成功")

@api.route("/college/update",methods=["POST"])
@login_required
@power_filter
def colleteUpdate():
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR, msg="未接收到数据")

    id = res_dir.get("id")
    name = res_dir.get("name")
    image = res_dir.get("image")
    site = res_dir.get("site")
    intro = res_dir.get("intro")
    level = res_dir.get("level")

    if not all([id,name,image,site,level]):
        return jsonify(code=RET.PARAMERR,msg="参数不完整")

    try:
        College.query.filter_by(id=id).update({"name":name,"image":image,"site":site,"intro":intro,"level":level})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="修改失败")

    return jsonify(code=RET.OK,msg="修改成功")

@api.route("/collete/list")
def colleteList():
    isSelect = request.args.get("isSelect")
    data = []
    if isSelect is not None and isSelect == "0":
        #下拉框模式
        colleteList = College.query.all()
        for collete in colleteList:
            select = College.getSelect(collete)
            data.append(select)
    else:
        #列表展示模式
        #筛选数据
        name = request.args.get("name")
        site = request.args.get("site")
        level = request.args.get("level")

        filterList = []

        if name is not None:
            filterList.append(College.name.like("%"+name+"%"))
        if site is not None:
            filterList.append(College.site == site)
        if level is not None:
            filterList.append(College.level == level)

        colleteList = College.query.filter(*filterList).all()

        for collete in colleteList:
            info = {
                "id":collete.id,
                "name":collete.name,
                "level":collete.level,
                "image":collete.image
            }
            data.append(info)

    return jsonify(code=RET.OK,msg="成功",data=data)

@api.route("/collete/detail/<int:id>")
def colleteDetail(id):
    college = College.query.get(id)

    if college is None:
        return jsonify(code=RET.DATAERR,msg="未查找到数据")

    getRoleList = college.role
    roleList = []
    for role in getRoleList:
        info = {
            "id":role.id,
            "name":role.name,
            "head_portrait":role.head_portrait
        }
        roleList.append(info)

    data = {
        "id":college.id,
        "name":college.name,
        "image":college.image,
        "intro":college.intro,
        "level":college.level,
        "role":roleList
    }

    return jsonify(code=RET.OK,msg="成功",data=data)
