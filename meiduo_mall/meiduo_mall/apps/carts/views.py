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
            pip.sadd('selected_' + key, sku_id)

            pip.execute()
            return JsonResponse({'code': 0, 'errmsg': 'OK'})
        # 5.未登录
        else:
            cart_str = request.COOKIES.get('carts')
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
            cart_str = base64.b64encode(pickle.dumps(cart_dic)).decode()
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
            redis_set = redis_cli.smembers('selected_' + str(user.id))
            cart_dict = {}
            for sku_id, count in redis_dict.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in redis_set
                }
        # 未登录
        else:
            cart_str = request.COOKIES.get('carts')
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

    def put(self, request):
        # 1.接受参数
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        count = dict.get('count')
        selected = dict.get('selected', True)
        print(selected)
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
        if selected:
            if not isinstance(selected, bool):
                return JsonResponse({'code': 400, 'errmsg': 'selected参数格式有误'})
        # 3.判断是否登录
        # 4.已登录
        if request.user.is_authenticated:
            redis_cli = get_redis_connection('carts')
            pip = redis_cli.pipeline()
            pip.hset('carts_' + key, sku_id, count)
            if selected:
                pip.sadd('selected_' + key, sku_id)
            else:
                pip.srem('selected_' + key, sku_id)
            pip.execute()
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'default_image_url': sku.default_image_url,
                'price': sku.price,
                'amount': sku.price * count,
            }
            return JsonResponse({'code': 0, 'errmsg': '修改购物车成功', 'cart_sku': cart_sku})
        # 5.未登录
        else:
            cart_str = request.COOKIES.get('carts')

            if cart_str:
                cart_dic = pickle.loads(base64.b64decode(cart_str))
            else:
                cart_dic = {}

            cart_dic[sku_id] = {
                'count': count,
                'selected': selected
            }
            cart_str = base64.b64encode(pickle.dumps(cart_dic)).decode()

            # 创建响应对象
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected
            }
            response = JsonResponse({'code': 0,
                                     'errmsg': '修改购物车成功',
                                     'cart_sku': cart_sku})
            # 响应结果并将购物车数据写入到cookie
            response.set_cookie('carts', cart_str)

            return response

    def delete(self, request):

        # 1.接受参数
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        key = str(request.user.id)
        # 2.验证参数
        try:
            sku = SKU.objects.get(pk=sku_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': 'sku_id错误'})
        # 3.判断是否登录
        # 4.已登录
        if request.user.is_authenticated:
            redis_cli = get_redis_connection('carts')
            pip = redis_cli.pipeline()
            pip.hdel('carts_' + key, sku_id)
            pip.srem('selected_' + key, sku_id)
            pip.execute()
            return JsonResponse({'code': 0,
                                 'errmsg': '删除购物车成功'})
        # 5.未登录
        else:
            cart_str = request.COOKIES.get('carts')

            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str))
            else:
                cart_dict = {}

            # 创建响应对象
            response = JsonResponse({'code': 0,
                                     'errmsg': '删除购物车成功'})
            if sku_id in cart_dict:
                del cart_dict[sku_id]
                cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
                response.set_cookie('carts', cart_str)
            return response


class CartSelectAllView(View):
    def put(self, request):
        # 1.接受参数
        dict = json.loads(request.body.decode())
        selected = dict.get('selected')
        key = str(request.user.id)
        # 2.验证
        if selected:
            if not isinstance(selected, bool):
                return JsonResponse({'code': 400, 'errmsg': 'selected参数格式有误'})
        # 3.判断是否登录
        # 4.已登录
        if request.user.is_authenticated:
            redis_cli = get_redis_connection('carts')
            dict = redis_cli.hgetall('carts_' + key)
            fields = dict.keys()
            if selected:
                redis_cli.sadd('selected_' + key, *fields)
            else:
                redis_cli.srem('selected_' + key, *fields)
            return JsonResponse({'code': 0, 'errmsg': 'OK'})
        # 5.未登录
        else:
            cart_str = request.COOKIES.get('carts')
            response = JsonResponse({'code': 0, 'errmsg': '全选购物车成功'})
            if cart_str:
                cart_dic = pickle.loads(base64.b64decode(cart_str))
                sku_id_keys = cart_dic.keys()
                for sku_id in sku_id_keys:
                    cart_dic[sku_id]['selected'] = selected
                cart_data = base64.b64encode(pickle.dumps(cart_dic)).decode()

                response.set_cookie('carts', cart_data)

            return response


class CartsSimpleView(View):

    def get(self, request):
        key = str(request.user.id)
        # 判断是否登录已登录
        if request.user.is_authenticated:
            # 链接redis
            redis_cli = get_redis_connection('carts')
            redis_dict = redis_cli.hgetall('carts_' + key)
            redis_set = redis_cli.smembers('selected_' + key)
            cart_dict = {}
            for sku_id, count in redis_dict.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in redis_set
                }
        # 未登录
        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str))
            else:
                cart_dict = {}
        cart_skus = []
        for sku_id, item in cart_dict.items():
            try:
                sku = SKU.objects.get(id=sku_id)
            except:
                return JsonResponse({'code': 400, 'errmsg': 'sku_id错误'})
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': cart_dict[sku.id]['count'],
                'default_image_url': sku.default_image_url
            })

        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'cart_skus': cart_skus})
