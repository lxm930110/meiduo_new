from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet


from meiduo_admin.serializer.permissiongroup import GroupModelSerializer, PermissionModelSerializer

from meiduo_admin.utils import PageNum


class GroupModelViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    pagination_class = PageNum

    def simple(self,request):
        obj = Permission.objects.all()
        ser = PermissionModelSerializer(obj,many=True)
        return Response(ser.data)



