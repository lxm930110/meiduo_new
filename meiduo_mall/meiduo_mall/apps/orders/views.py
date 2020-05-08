from datetime import datetime
from _decimal import Decimal

from django import http
from django.shortcuts import render
from django.utils import timezone
from django_redis import get_redis_connection
from django.http import JsonResponse
from django.views import View
import json
from django.db import transaction
from goods.models import SKU
from meiduo_mall.utils.info import InfoMixin
from orders.models import OrderInfo, OrderGoods
from users.models import Address


class OrderSettlementView(InfoMixin, View):

    def get(self, request):
        key = str(request.user.id)
        # 1.获取地址
        try:
            addresses = Address.objects.filter(user=request.user, is_deleted=False)
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
        sku_dict_byte = redis_cli.hgetall('carts_' + key)
        sku_set_byte = redis_cli.smembers('selected_' + key)
        # pip.execute()
        print(sku_dict_byte)
        sku_dict = {int(sku_id): int(count) for sku_id, count in sku_dict_byte.items()}
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

        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'context': context})


class OrderCommitView(View):
    def post(self, request):
        dict = json.loads(request.body.decode())
        address_id = dict.get('address_id')
        pay_method = dict.get('pay_method')
        # 校验参数
        if not all([address_id, pay_method]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        # 判断address_id是否合法
        try:
            address = Address.objects.get(id=address_id)
        except Exception:
            return JsonResponse({'code': 400, 'errmsg': '参数address_id错误'})
        # 判断pay_method是否合法
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return JsonResponse({'code': 400, 'errmsg': '参数pay_method错误'})
        # 从 redis 读取购物车中被勾选的商品信息
        key = str(request.user.id)
        redis_cli = get_redis_connection('carts')
        sku_id_dict_byte = redis_cli.hgetall('carts_' + key)
        selected_set_byte = redis_cli.smembers('selected_' + key)
        sku_id_dict = {int(sku_id): int(count) for sku_id, count in sku_id_dict_byte.items()}
        selected_list = [int(count) for count in selected_set_byte]
        # 获取登录用户
        user = request.user
        # 关闭事务自动提交
        with transaction.atomic():
            # 开启事务
            sid = transaction.savepoint()
            # 生成订单编号
            order_id = '%s%09d' % (datetime.now().strftime('%Y%m%d%H%M%S'), user.id)
            # 保存订单基本信息 OrderInfo（一）
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address,
                total_count=0,
                total_amount=0,
                freight=10,
                pay_method=pay_method,
                status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY']
                else OrderInfo.ORDER_STATUS_ENUM['UNSEND']
            )
            skus = SKU.objects.filter(pk__in=selected_list)
            for sku in skus:
                sku_count = sku_id_dict[sku.id]
                if sku_count > sku.stock:
                    # 事务回滚
                    transaction.savepoint_rollback(sid)

                    return JsonResponse({'code': 400, 'errmsg': '库存不足'})
                # # 修改商品库存
                # sku.stock -= sku_count
                # # 修改商品销量
                # sku.sales += sku_count
                # sku.save()
                sku_stock_old = sku.stock
                stock_new =sku.stock - sku_count
                sales_new = sku.sales + sku_count
                # 添加乐观锁
                result = SKU.objects.filter(pk=sku.id, stock=sku_stock_old).update(stock=stock_new,sales=sales_new)
                if result == 0:
                    return JsonResponse({'code': 400, 'errmsg': '服务器繁忙，请稍后'})
                # 修改商品类型销量
                sku.goods.sales += sku_count
                sku.goods.save()
                # 保存订单商品信息 OrderGoods（多）
                OrderGoods.objects.create(
                    order=order,
                    sku=sku,
                    count=sku_count,
                    price=sku.price,
                )
                order.total_count += sku_count
                order.total_amount += (sku_count * sku.price)

            # 添加邮费和保存订单信息
            order.total_amount += order.freight
            order.save()
        # 事务提交
        transaction.savepoint_commit(sid)

        # 清除购物车中已结算的商品
        redis_cli.hdel('carts_%s' % user.id, *selected_list)
        redis_cli.srem('selected_%s' % user.id, *selected_list)

        # 响应提交订单结果
        return JsonResponse({'code': 0,
                             'errmsg': '下单成功',
                             'order_id': order.order_id})





