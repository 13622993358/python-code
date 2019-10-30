from . import api
from flask import request,jsonify,current_app
from app.utils.response_code import RET
from app.utils.common import login_required,power_filter
from app.model import Banner,db

@api.route("/banner/add",methods=["POST"])
@login_required
@power_filter
def bannerAdd():
    '''
    新增轮播图
    :return:状态
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return jsonify(code=RET.PARAMERR, msg="未接收到数据")

    image = res_dir.get("image")
    link_url = res_dir.get("link_url")

    if image is None:
        return jsonify(code=RET.PARAMERR, msg="请选择上传图片")

    banner = Banner(image=image,link_url=link_url)

    try:
        db.session.add(banner)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="新增失败")

    return jsonify(code=RET.OK,msg="成功")

@api.route("/banner/delete/<int:id>")
@login_required
@power_filter
def bannerDelete(id):
    '''
    删除轮播图
    :param id:
    :return:状态
    '''
    banner = Banner.query.get(id)
    if banner is None:
        return jsonify(code=RET.PARAMERR,msg="查找不到删除数据")

    try:
        db.session.delete(banner)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="删除失败")

    return jsonify(code=RET.OK,msg="成功")

@api.route("/banner/list")
def bannerList():
    '''
    轮播图列表
    :return:list
    '''
    banner = Banner.query.all()
    data = []
    for i in banner:
        info = {
            "id":i.id,
            "image":i.image,
            "link_url":i.link_url
        }
        data.append(info)

    return jsonify(code=RET.OK,data=data,msg="成功")

@api.route("/banner/detail/<int:id>")
def bannerDetail(id):
    '''
    轮播图详情
    :return:
    '''
    banner = Banner.query.get(id)
    if banner is None:
        return jsonify(code=RET.DATAERR,msg="查找不到数据")

    data = {
        "id":banner.id,
        "image":banner.image,
        "link_url":banner.link_url,
        "update_time":banner.update_time
    }

    return jsonify(code=RET.OK,msg="成功",data=data)

@api.route("/banner/update",methods=["POST"])
@login_required
@power_filter
def bannerUpdate():
    '''
    轮播图更新
    :return:
    '''
    res_dir = request.get_json()

    if res_dir is None:
        return jsonify(code=RET.PARAMERR,msg="未接收到参数")

    id = res_dir.get("id")
    image = res_dir.get("image")
    link_url = res_dir.get("link_url")

    if not all([id,image]):
        return jsonify(code=RET.PARAMERR,msg="参数不完整")

    try:
        Banner.query.filter_by(id=id).update({"image":image,"link_url":link_url if link_url is not None else ""})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATAERR,msg="修改失败")

    return jsonify(code=RET.OK,msg="成功")