from rest_framework import serializers

from goods.models import SKU, SKUSpecification


class SkuSpecificationModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKUSpecification
        fields = ['option_id','spec_id']



class SkuModelSerializer(serializers.ModelSerializer):
    # 获取关联对象名
    goods = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    # 获取关联id
    goods_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    # 获取sepc
    skuspecification_set = SkuSpecificationModelSerializer(many=True)


    class Meta:
        model = SKU
        fields = '__all__'