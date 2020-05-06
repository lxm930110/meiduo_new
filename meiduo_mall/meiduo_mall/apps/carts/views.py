import pickle, base64

from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django_redis import get_redis_connection
from django.http import JsonResponse
import json

from goods.models import SKU


class AddCarts(View):

    def post(self, request):
        # 1.接受参数
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        count = dict.get('count')
        selected = dict.get('selected', True)
        key = str(request.user.id)
        # 2.验证参数
        if not all([sku_id, count]):
            return JsonResponse({'code': 400, 'errmsg': '参数不完整'})
        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': 'sku_id错误'})
        count = int(count)
        if count > sku.stock:
            return JsonResponse({'code': 400, 'errmsg': '库存不足'})
        # 3.判断是否登录
        # 4.已登录
        if request.user.is_authenticated:
            redis_cli = get_redis_connection('carts')
            pip = redis_cli.pipeline()

            pip.hincrby('carts_' + key, sku_id, count)
            pip.sadd('selecteds_' + key, sku_id)

            pip.execute()
            return JsonResponse({'code': 0, 'errmsg': 'OK'})
        # 5.未登录
        else:
            cart_str = request.Cookie.get('carts')
            if cart_str:
                cart_dic = pickle.loads(base64.b64decode(cart_str))
            else:
                cart_dic = {}
            if sku_id in cart_dic:
                count += cart_dic[sku_id]['count']
            cart_dic[sku_id] = {
                'count': count,
                'selected': True
            }
            cart_str = base64.b16encode(pickle.dumps(cart_dic)).decode()
            response = JsonResponse({'code': 0, 'errmsg': 'OK'})

            response.set_cookie('carts', cart_str, max_age=60 * 60 * 24 * 7)
            return response

    def get(self, request):
        user = request.user
        # 判断是否登录
        # 已登录
        if user.is_authenticated:
            redis_cli = get_redis_connection('carts')
            redis_dict = redis_cli.hgetall('carts_' + str(user.id))
            redis_set = redis_cli.smembers('selecteds_' + str(user.id))
            cart_dict = {}
            for sku_id, count in redis_dict.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in redis_set
                }
        # 未登录
        else:
            cart_str = request.COOKIE.get('carts')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str))
            else:
                cart_dict = {}
        skus_id = cart_dict.keys()
        cart_skus = []
        for sku_id in skus_id:
            try:
                sku = SKU.objects.get(id=sku_id)
            except:
                return JsonResponse({'code': 400, 'errmsg': 'sku_id错误'})
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': cart_dict.get(sku.id).get('count'),
                'selected': cart_dict.get(sku.id).get('selected'),
                'default_image_url': sku.default_image_url,
                'price': sku.price,
            })
        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'cart_skus': cart_skus})
