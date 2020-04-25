
from itsdangerous.jws import TimedJSONWebSignatureSerializer

from django.conf import settings


def dumps(openid):
    '''
    将字典加密，返回加密字符串
    :param json: 字典
    :return: 字符串
    '''
    # 实例化
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=60*10)
    data = {'openid': openid}
    token_str = serializer.dumps(data).decode()
    return token_str


def loads(access_token):
    '''
    将加密字符串解密
    :param json_str: 加密字符串
    :return: 字典
    '''
    # 实例化
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=60*10)
    try:
        # 解码获取openid
        openid = serializer.loads(access_token)
    except:
        # 如果字符串被修改过，或超期，会抛异常
        return None
    else:
        return openid
