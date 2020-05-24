from fdfs_client.client import Fdfs_client
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from goods.models import SKUImage, SKU
from meiduo_admin.serializer.imageserializer import ImageModelSerializer, SimpleModelSerializer
from meiduo_admin.utils import PageNum


class ImageModelViewSet(ModelViewSet):

    queryset = SKUImage.objects.all()

    serializer_class = ImageModelSerializer

    pagination_class = PageNum

    def create(self, request, *args, **kwargs):
        sku_id = request.data.get('sku')
        new_image = request.FILES.get('image')

        client = Fdfs_client('meiduo_mall/utils/fastdfs/client.conf')

        result = client.upload_by_buffer(new_image.read())

        if result.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FDFS系统失败')

        image_url = result.get('Remote file_id')

        # 保存图片
        img = SKUImage.objects.create(sku_id=sku_id, image=image_url)

        return Response(
            {
                'image': img.image.url,
                'id': img.id,
                'sku': sku_id,

            },
            status=201  # 前端需要接受201状态
        )

    def update(self, request, *args, **kwargs):
        sku_id = request.data.get('sku')
        picture = request.FILES.get('image')
        pk = kwargs['pk']
        client = Fdfs_client('meiduo_mall/utils/fastdfs/client.conf')

        result = client.upload_by_buffer(picture.read())

        if result.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FDFS系统失败')

        image_url = result.get('Remote file_id')

        # 保存图片
        obj = SKUImage.objects.get(pk=pk)
        obj.image = image_url
        obj.save()
        return Response(
            {
                'image': obj.image.url,
                'id': obj.id,
                'sku': sku_id,

            },
            status=201  # 前端需要接受201状态
        )


# 获取skus　imple列表
class SimpleListAPIView(ListAPIView):

    queryset = SKU.objects.all()
    serializer_class = SimpleModelSerializer
