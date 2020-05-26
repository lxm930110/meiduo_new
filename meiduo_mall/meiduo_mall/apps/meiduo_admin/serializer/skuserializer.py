from rest_framework import serializers

from goods.models import SKU, SKUSpecification, GoodsCategory, Goods, SpecificationOption, GoodsSpecification

from django.db import transaction



# 获取规格序列器
class SkuSpecificationModelSerializer(serializers.ModelSerializer):

    option_id = serializers.IntegerField()
    spec_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ['option_id','spec_id']


class SkuModelSerializer(serializers.ModelSerializer):
    # 获取关联对象名
    spu = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    # 获取关联id
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    # 获取sepc
    specs = SkuSpecificationModelSerializer(many=True)

    class Meta:
        model = SKU
        fields = '__all__'

    # 重写create方法分别保存sku和skuspecifcation
    def create(self, validated_data):
        specs = validated_data.pop('specs')
        # 事务
        with transaction.atomic():
            #　创建事务
            sp = transaction.savepoint()
            sku = SKU.objects.create(**validated_data)
            for spec in specs:
                SKUSpecification.objects.create(sku=sku, **spec)
            # 提交事务
            transaction.savepoint_commit(sp)
            return sku


    # 重写create方法分别保存sku和skuspecifcation
    def update(self, instance, validated_data):
        specs = validated_data.pop('specs')
        # 事务
        with transaction.atomic():
            #　创建事务
            sp = transaction.savepoint()
            super().update(instance,validated_data)
            for spec in specs:
                SKUSpecification.objects.filter(sku=instance,spec_id=spec.get('spec_id')).update(option_id = spec.get('option_id'))
            # 提交事务
            transaction.savepoint_commit(sp)
            return instance



# 三级分类序列化器
class GoodsCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields ='__all__'




# 获取具体规格选项序列器
class SpecificationOptionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecificationOption
        fields = ['id','value']


# 获取规格序列器
class GoodsSpecificationModelSerializer(serializers.ModelSerializer):

    options = SpecificationOptionModelSerializer(many=True)
    spu_id = serializers.IntegerField()

    class Meta:
        model = GoodsSpecification
        fields = '__all__'


# SPU序列化器
class GoodsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ['id','name']