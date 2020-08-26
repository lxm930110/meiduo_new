from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from django.views import View

from areas.models import Areas
from django.http import JsonResponse, HttpResponse


class AreasView(View):

    def get(self, request):
        # 获取缓存中的province_list
        province_list1 = cache.get('province_list1')
        # 判断是否有缓存
        if not province_list1:
            try:
                # 查询省份数据
                province_list = Areas.objects.filter(parent__isnull=True)
                province_list1 = []
                for province in province_list:
                    province_list1.append({'id': province.id, 'name': province.name})
                # 缓存省份数据
                cache.set('province_list1', province_list1, 60 * 60)
            except:
                return JsonResponse({'code': 400, 'errmsg': '查询数据库出错'})

        return JsonResponse({'code': 0, 'errmsg': 'OK', 'province_list': province_list1})


class SubsAreasView(View):

    def get(self, request, pk):
        if not pk:
            return JsonResponse({'code': 400, 'errmsg': '参数不存在'})
        sub_data = cache.get('sub_area_' + pk)
        # 判断是否有缓存
        if not sub_data:
            try:
                province_city = Areas.objects.get(id=pk)
                # 查询市或区数据
                city_list = province_city.subs.all()
                city_list1 = []
                for city in city_list:
                    city_list1.append({'id': city.id, 'name': city.name})
                sub_data = {'id': province_city.id, 'name': province_city.name, 'subs': city_list1}
                # 缓存市或区数据
                cache.set('sub_area_' + pk, sub_data, 60 * 60)
            except:
                return JsonResponse({'code': 400, 'errmsg': '查询数据库出错'})
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'sub_data': sub_data})
