from rest_framework import serializers
from goods.models import SKUImage,SKU


class ImageModelSerializer(serializers.ModelSerializer):

    sku = serializers.StringRelatedField()

    class Meta:
        model = SKUImage
        fields = ['id','sku','image']


class SimpleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = ['id','name']
