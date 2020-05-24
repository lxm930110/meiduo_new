from rest_framework.viewsets import ModelViewSet

from goods.models import SKU
from meiduo_admin.serializer.skuserializer import SkuModelSerializer
from meiduo_admin.utils import PageNum


class SkuSetView(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SkuModelSerializer
    pagination_class = PageNum
