from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods

# 订单序列化
class OrderModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderInfo
        fields = ['order_id','create_time']



################################################

# sku序列化
class SkuModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = SKU

        fields = ['name','default_image_url']


# ordergood序列化
class SkuGoodModelSerializer(serializers.ModelSerializer):

    sku = SkuModelSerializer(read_only=True)

    class Meta:

        model = OrderGoods
        fields = ['price','count','sku']



# orderinfo序列化
class OrderDetailModelSerializer(serializers.ModelSerializer):

    skus = SkuGoodModelSerializer(many=True,read_only=True)

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderInfo
        exclude = ('address',)


