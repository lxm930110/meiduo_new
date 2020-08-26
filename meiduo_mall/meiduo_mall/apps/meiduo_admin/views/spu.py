from goods.models import Goods, Brand, GoodsCategory
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializer.skuserializer import GoodsCategoryModelSerializer
from meiduo_admin.serializer.spu import SPUModelSerializer, BrandModelSerializer
from meiduo_admin.utils import PageNum
from rest_framework.generics import ListAPIView


class SPUModelViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = SPUModelSerializer
    pagination_class = PageNum

    def get_queryset(self):

        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:

            return Goods.objects.all()
        else:

            return Goods.objects.filter(order_id=keyword)


# 获取品牌列表

class GoodsBrandListAPIView(ListAPIView):

    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer

# GoodsCategory


# 获取商品1分类列表
class GoodsCategory1ListAPIView(ListAPIView):

    queryset = GoodsCategory.objects.filter(parent=None)
    serializer_class = GoodsCategoryModelSerializer



# 获取商品2/3分类列表
class Goods2Category3ListAPIView(ListAPIView):


    serializer_class = GoodsCategoryModelSerializer

    def get_queryset(self):


        pk = self.kwargs.get('pk')

        return GoodsCategory.objects.filter(parent_id=pk)