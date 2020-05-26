from goods.models import SpecificationOption,GoodsSpecification
from rest_framework import serializers


class SpecificationOptionModelSerializer(serializers.ModelSerializer):

    spec_id = serializers.IntegerField()
    spec = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SpecificationOption
        fields = '__all__'



class SpecOptionModelSerializer(serializers.ModelSerializer):
    # spu_id = serializers.IntegerField()
    # spu = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GoodsSpecification
        fields = '__all__'

