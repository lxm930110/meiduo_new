from rest_framework.generics import ListCreateAPIView

from meiduo_admin.serializer.userserializer import UserModelSerializer

from users.models import User

from meiduo_admin.utils import PageNum


class UserView(ListCreateAPIView):
    '''
    分页获取用户信息和查询获取
    '''
    # queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # 分页
    pagination_class = PageNum

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:

            return User.objects.all()
        else:
            return User.objects.filter(username=keyword)

