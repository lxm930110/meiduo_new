
from goods.models import GoodsChannel
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializer.Channel import GoodsChannelModelSerializer

from meiduo_admin.utils import PageNum


class GoodsChannelModelViewSet(ModelViewSet):
    queryset = GoodsChannel.objects.all()
    serializer_class = GoodsChannelModelSerializer
    pagination_class = PageNum

    # def channel_types(self,request):

