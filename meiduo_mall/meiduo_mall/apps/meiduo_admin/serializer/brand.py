from goods.models import Goods,Brand
from rest_framework import serializers


class BrandModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'
