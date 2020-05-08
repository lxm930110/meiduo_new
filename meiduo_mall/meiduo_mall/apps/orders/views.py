from _decimal import Decimal

from django.shortcuts import render
from django_redis import get_redis_connection
from django.http import JsonResponse
from django.views import View

from goods.models import SKU
from meiduo_mall.utils.info import InfoMixin
from users.models import Address


class OrderSettlementView(InfoMixin,View):

    def get(self, request):
        key = str(request.user.id)
        # 1.获取地址
        try:
            addresses = Address.objects.filter(user=request.user,is_deleted=False)
        except Address.DoesNotExist:
            addresses = None
        list1 = []
        for address in addresses:
            list1.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile
            })
        # 2.链接redis获取商品信息
        redis_cli = get_redis_connection('carts')
        sku_dict_byte = redis_cli.hgetall('carts_'+key)
        sku_set_byte = redis_cli.smembers('selected_'+key)
        # pip.execute()
        print(sku_dict_byte)
        sku_dict = {int(sku_id):int(count) for sku_id,count in sku_dict_byte.items()}
        sku_list = [int(sku_id) for sku_id in sku_set_byte]
        skus = SKU.objects.filter(pk__in=sku_list)
        list = []
        for sku in skus:
            list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image_url,
                'count': sku_dict[sku.id],
                'price': sku.price
            })
        # 补充运费
        freight = Decimal('10.00')
        # 渲染界面
        context = {
            'addresses': list1,
            'skus': list,
            'freight': freight,
        }

        return JsonResponse({'code':0,
                                  'errmsg':'ok',
                                  'context':context})


