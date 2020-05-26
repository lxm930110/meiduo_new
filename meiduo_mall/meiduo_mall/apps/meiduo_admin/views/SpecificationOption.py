
from goods.models import SpecificationOption,GoodsSpecification
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from meiduo_admin.serializer.specificationoption import SpecificationOptionModelSerializer, SpecOptionModelSerializer
from meiduo_admin.utils import PageNum


# 规格选项
class SpecificationOptionModelViewSet(ModelViewSet):
    queryset = SpecificationOption.objects.all()
    serializer_class = SpecificationOptionModelSerializer
    pagination_class = PageNum


# /specs/simple
class SpecOptionListAPIView(ListAPIView):
    queryset = GoodsSpecification.objects.all()
    serializer_class = SpecOptionModelSerializer