from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from goods.models import SKU, GoodsCategory, Goods,GoodsSpecification
from meiduo_admin.serializer.skuserializer import SkuModelSerializer, GoodsCategoryModelSerializer, \
    GoodsModelSerializer, GoodsSpecificationModelSerializer
from meiduo_admin.utils import PageNum


# 获取三级分类列表
class GoodsCategory3ListAPIView(ListAPIView):
    serializer_class = GoodsCategoryModelSerializer
    queryset = GoodsCategory.objects.filter(goodscategory=None)


# 获取SPU列表
class GoodsListAPIView(ListAPIView):
    serializer_class = GoodsModelSerializer
    queryset = Goods.objects.all()



# 获取spu规格
class SpuListAPIView(ListAPIView):
    serializer_class = GoodsSpecificationModelSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return GoodsSpecification.objects.filter(spu_id=pk)







class SkuSetView(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SkuModelSerializer
    pagination_class = PageNum




