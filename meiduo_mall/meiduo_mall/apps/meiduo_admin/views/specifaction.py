
from goods.models import GoodsSpecification
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializer.specifaction import GoodsSpecificationModelSerializer
from meiduo_admin.utils import PageNum



class SpecificationModelViewSet(ModelViewSet):
    queryset = GoodsSpecification.objects.all()
    serializer_class = GoodsSpecificationModelSerializer
    pagination_class = PageNum