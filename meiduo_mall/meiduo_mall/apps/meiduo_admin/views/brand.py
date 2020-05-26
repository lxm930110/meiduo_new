
from goods.models import Brand
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializer.brand import BrandModelSerializer

from meiduo_admin.utils import PageNum


class BrandModelViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    pagination_class = PageNum

    # def channel_types(self,request):

