from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.Province.models import Province
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台省份添加
    def get(self,request):

        # 使用模板
        return render(request, 'Province/province_frontAdd.html')

    def post(self, request):
        province = Province() # 新建一个省份对象然后获取参数
        province.provinceName = request.POST.get('province.provinceName')
        province.save() # 保存省份信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改省份
    def get(self, request, provinceId):
        context = {'provinceId': provinceId}
        return render(request, 'Province/province_frontModify.html', context)


class FrontListView(BaseView):  # 前台省份查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        provinces = Province.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(provinces, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        provinces_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'provinces_page': provinces_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Province/province_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示省份详情页
    def get(self, request, provinceId):
        # 查询需要显示的省份对象
        province = Province.objects.get(provinceId=provinceId)
        context = {
            'province': province
        }
        # 渲染模板显示
        return render(request, 'Province/province_frontshow.html', context)


class ListAllView(View): # 前台查询所有省份
    def get(self,request):
        provinces = Province.objects.all()
        provinceList = []
        for province in provinces:
            provinceObj = {
                'provinceId': province.provinceId,
                'provinceName': province.provinceName,
            }
            provinceList.append(provinceObj)
        return JsonResponse(provinceList, safe=False)


class UpdateView(BaseView):  # Ajax方式省份更新
    def get(self, request, provinceId):
        # GET方式请求查询省份对象并返回省份json格式
        province = Province.objects.get(provinceId=provinceId)
        return JsonResponse(province.getJsonObj())

    def post(self, request, provinceId):
        # POST方式提交省份修改信息更新到数据库
        province = Province.objects.get(provinceId=provinceId)
        province.provinceName = request.POST.get('province.provinceName')
        province.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台省份添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'Province/province_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        province = Province() # 新建一个省份对象然后获取参数
        province.provinceName = request.POST.get('province.provinceName')
        province.save() # 保存省份信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新省份
    def get(self, request, provinceId):
        context = {'provinceId': provinceId}
        return render(request, 'Province/province_modify.html', context)


class ListView(BaseView):  # 后台省份列表
    def get(self, request):
        # 使用模板
        return render(request, 'Province/province_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        provinces = Province.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(provinces, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        provinces_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        provinceList = []
        for province in provinces_page:
            province = province.getJsonObj()
            provinceList.append(province)
        # 构造模板页面需要的参数
        province_res = {
            'rows': provinceList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(province_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除省份信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        provinceIds = self.getStrParam(request, 'provinceIds')
        provinceIds = provinceIds.split(',')
        count = 0
        try:
            for provinceId in provinceIds:
                Province.objects.get(provinceId=provinceId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出省份信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        provinces = Province.objects.all()
        #将查询结果集转换成列表
        provinceList = []
        for province in provinces:
            province = province.getJsonObj()
            provinceList.append(province)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(provinceList)
        # 设置要导入到excel的列
        columns_map = {
            'provinceId': '省份id',
            'provinceName': '省份名称',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'provinces.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="provinces.xlsx"'
        return response

