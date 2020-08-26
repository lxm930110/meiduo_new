import base64,pickle
from django_redis import get_redis_connection

def mergey_carts(request, response):

    # 1.在cookie中获取未登录购物车数据
    cart_str = request.COOKIES.get('carts')
    key = str(request.user.id)
    # 2.判断数据是否存在
    if not cart_str:
        return response
    # 解密难道字典数据
    cart_dic = pickle.loads(base64.b64decode(cart_str))
    # 链接redis
    redis_cli = get_redis_connection('carts')
    pip = redis_cli.pipeline()
    for sku_id,item in cart_dic.items():

       pip.hincrby('carts_'+key,sku_id,item['count'])
       if item['selected']:
           pip.sadd('selected_'+key,sku_id)
       else:
           pip.srem('selected_'+key,sku_id)
    pip.execute()
    response.delete_cookie('carts')
    return response