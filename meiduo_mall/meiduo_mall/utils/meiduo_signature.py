
from itsdangerous.jws import TimedJSONWebSignatureSerializer

from django.conf import settings


def dumps(data, expires):
    '''
    将字典加密，返回加密字符串
    :param json: 字典
    :return: 字符串
    '''
    # 实例化
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=expires)
    data_dict_str = serializer.dumps(data).decode()
    return data_dict_str


def loads(data, expires):
    '''
    将加密字符串解密
    :param json_str: 加密字符串
    :return: 字典
    '''
    # 实例化
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=expires)
    try:
        # 解码获取openid
        data_dict = serializer.loads(data)
    except:
        # 如果字符串被修改过，或超期，会抛异常
        return None
    else:
        return data_dict
