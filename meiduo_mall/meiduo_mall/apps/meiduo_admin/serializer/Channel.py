from goods.models import GoodsChannel
from rest_framework import serializers


class GoodsChannelModelSerializer(serializers.ModelSerializer):

    category_id = serializers.IntegerField()
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GoodsChannel
        fields = '__all__'

