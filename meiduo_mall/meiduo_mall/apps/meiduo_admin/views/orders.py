from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from meiduo_admin.serializer.orderserializer import OrderDetailModelSerializer, OrderModelSerializer
from meiduo_admin.utils import PageNum
from orders.models import OrderInfo


# class OrderListAPIView(ListAPIView):
#     queryset = OrderInfo.objects.all()
#     serializer_class = OrderModelSerializer
#     pagination_class = PageNum
#
#     def get_queryset(self):
#
#         keyword = self.request.query_params.get('keyword')
#
#         if keyword == '' or keyword is None:
#
#             return OrderInfo.objects.all()
#         else:
#
#             return OrderInfo.objects.filter(order_id=keyword)


# class OrderDetailListAPIView(RetrieveAPIView):
#     queryset = OrderInfo.objects.all()
#     serializer_class = OrderDetailModelSerializer



class OrderReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderDetailModelSerializer
    pagination_class = PageNum

    def get_queryset(self):

        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:

            return OrderInfo.objects.all()
        else:

            return OrderInfo.objects.filter(order_id=keyword)

    @action(methods=['put'],detail=True)
    def status(self,request,pk):
        status = request.data.get('status')
        obj = self.get_object()
        obj.status = status
        obj.save()
        ser = self.get_serializer(obj)
        return Response(ser.data)


