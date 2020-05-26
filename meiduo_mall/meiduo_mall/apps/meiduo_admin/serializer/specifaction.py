from goods.models import Goods,GoodsSpecification
from rest_framework import serializers


class GoodsSpecificationModelSerializer(serializers.ModelSerializer):

    spu_id = serializers.IntegerField()
    spu = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GoodsSpecification
        fields = '__all__'
