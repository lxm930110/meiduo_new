from django.contrib.auth.models import Permission,ContentType
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializer.permission import PermissionModelSerializer, ContentTypeModelSerializer

from meiduo_admin.utils import PageNum


class PermissionModelViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionModelSerializer
    pagination_class = PageNum

    def content_types(self,request):
        obj = ContentType.objects.all()
        ser = ContentTypeModelSerializer(obj,many=True)
        return Response(ser.data)



