from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from goods.models import GoodsVisitCount
from meiduo_admin.serializer.statisticalserializer import GoodsVisitCountModelSerializer
from users.models import User
from datetime import date,timedelta
from rest_framework.response import Response

class StatisticalCountUser(APIView):
    '''
    统计所有用户
    '''
    permission_classes = [IsAdminUser]

    def get(self,request):
        # 获取个数
        count = User.objects.all().count()
        #　获取当日时间
        new_date = date.today()

        return Response({
            'count':count,
            'date':new_date
            })

class StatisticalCountActiveUser(APIView):
    '''
    统计活跃用户
    '''
    permission_classes = [IsAdminUser]

    def get(self,request):

        # 　获取当日时间
        new_date = date.today()
        # 获取个数
        count = User.objects.filter(last_login__gte=new_date).count()

        return Response({
            'count':count,
            'date':new_date
            })

class StatisticalCountincrementUser(APIView):
    '''
    统计日增用户
    '''
    permission_classes = [IsAdminUser]

    def get(self,request):

        # 　获取当日时间
        new_date = date.today()
        # 获取个数
        count = User.objects.filter(date_joined__gte=new_date).count()

        return Response({
            'count':count,
            'date':new_date
            })

class StatisticalCountOrdersUser(APIView):
    '''
    统计下单用户
    '''
    permission_classes = [IsAdminUser]

    def get(self,request):

        # 　获取当日时间
        new_date = date.today()
        # 获取个数
        count = User.objects.filter(orderinfo__create_time__gte=new_date).count()

        return Response({
            'count':count,
            'date':new_date
            })


class StatisticalMonthCountUser(APIView):
    '''
    统计月增用户
    '''
    permission_classes = [IsAdminUser]

    def get(self,request):

        # 　获取当日时间
        new_date = date.today()
        index_date = new_date - timedelta(days=29)
        list_date = []
        for i in range(30):
            first_date = index_date + timedelta(days=i)
            second_date = first_date + timedelta(days=1)
            # 获取个数
            count = User.objects.filter(date_joined__gte=first_date,date_joined__lt=second_date).count()

            list_date.append({'count':count,
                            'date':first_date})

        return Response(list_date)


class StatisticalCountDetailVisitUser(APIView):
    '''
    统计商品访
    '''
    permission_classes = [IsAdminUser]

    def get(self,request):

        # 　获取当日时间
        new_date = date.today()
        # 获取个数

        goodvisitcount = GoodsVisitCount.objects.filter(create_time__gte=new_date)

        serializer = GoodsVisitCountModelSerializer(goodvisitcount, many=True)

        return Response(serializer.data)

