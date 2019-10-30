from . import api
from flask import request,current_app,jsonify
from app.utils.response_code import RET
from app.utils.img_store import storage
from app.utils.const import imgUrl

@api.route("/uploadImg",methods=["POST"])
def uploadImg():
    file = request.files.get("file")
    if file is None:
        return jsonify(code=RET.PARAMERR,msg="请选择上传文件")

    imgFile = file.read()

    try:
        key = storage(imgFile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.THIRDERR,msg="上传失败")

    url = imgUrl + key

    return jsonify(code=RET.OK,data=url,msg="成功")