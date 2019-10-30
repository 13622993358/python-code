from qiniu import Auth,put_data

# 需要填写你的 Access Key 和 Secret Key
access_key = 'bB6ELBlnjHwnGcv3NAphqH3APKezfnk1_KeWi_nl'
secret_key = 'SxB-Dtoox86WM88uJuPoaz5JJSrkeakTHTKYjiqA'

def storage(file_data):
    '''
    上传文件到七牛
    :param file_data:
    :return:key
    '''
    q = Auth(access_key,secret_key)

    #要上传的空间

    bucket_name = 'supernovas'

    token = q.upload_token(bucket_name,None,3600)

    ret,info = put_data(token,None,file_data)

    if info.status_code == 200:
        #200表示上传成功
        return ret.get("key")
    else:
        return Exception('上传七牛失败')