from goods.models import Goods, Brand, GoodsCategory
from rest_framework import serializers

# spu

class SPUModelSerializer(serializers.ModelSerializer):

    brand_id = serializers.IntegerField()
    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()

    brand = serializers.StringRelatedField(read_only=True)
    category1 = serializers.StringRelatedField(read_only=True)
    category2 = serializers.StringRelatedField(read_only=True)
    category3 = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Goods

        fields = '__all__'

# brand
class BrandModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand

        fields = '__all__'


# category1
class GoodsCategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory

        fields = '__all__'