from django.contrib.auth.models import Group

from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializer.admin import UserModelSerializer, GroupModelSerializer

from meiduo_admin.utils import PageNum

from users.models import User


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.filter(is_superuser=True,is_staff=True)
    serializer_class = UserModelSerializer
    pagination_class = PageNum

    def groups_simple(self,request):
        obj = Group.objects.all()
        ser = GroupModelSerializer(obj,many=True)
        return Response(ser.data)



