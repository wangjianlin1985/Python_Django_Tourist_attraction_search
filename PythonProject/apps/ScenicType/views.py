from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.ScenicType.models import ScenicType
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台景区类型添加
    def get(self,request):

        # 使用模板
        return render(request, 'ScenicType/scenicType_frontAdd.html')

    def post(self, request):
        scenicType = ScenicType() # 新建一个景区类型对象然后获取参数
        scenicType.typeName = request.POST.get('scenicType.typeName')
        scenicType.save() # 保存景区类型信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改景区类型
    def get(self, request, typeId):
        context = {'typeId': typeId}
        return render(request, 'ScenicType/scenicType_frontModify.html', context)


class FrontListView(BaseView):  # 前台景区类型查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        scenicTypes = ScenicType.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(scenicTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        scenicTypes_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'scenicTypes_page': scenicTypes_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'ScenicType/scenicType_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示景区类型详情页
    def get(self, request, typeId):
        # 查询需要显示的景区类型对象
        scenicType = ScenicType.objects.get(typeId=typeId)
        context = {
            'scenicType': scenicType
        }
        # 渲染模板显示
        return render(request, 'ScenicType/scenicType_frontshow.html', context)


class ListAllView(View): # 前台查询所有景区类型
    def get(self,request):
        scenicTypes = ScenicType.objects.all()
        scenicTypeList = []
        for scenicType in scenicTypes:
            scenicTypeObj = {
                'typeId': scenicType.typeId,
                'typeName': scenicType.typeName,
            }
            scenicTypeList.append(scenicTypeObj)
        return JsonResponse(scenicTypeList, safe=False)


class UpdateView(BaseView):  # Ajax方式景区类型更新
    def get(self, request, typeId):
        # GET方式请求查询景区类型对象并返回景区类型json格式
        scenicType = ScenicType.objects.get(typeId=typeId)
        return JsonResponse(scenicType.getJsonObj())

    def post(self, request, typeId):
        # POST方式提交景区类型修改信息更新到数据库
        scenicType = ScenicType.objects.get(typeId=typeId)
        scenicType.typeName = request.POST.get('scenicType.typeName')
        scenicType.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台景区类型添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'ScenicType/scenicType_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        scenicType = ScenicType() # 新建一个景区类型对象然后获取参数
        scenicType.typeName = request.POST.get('scenicType.typeName')
        scenicType.save() # 保存景区类型信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新景区类型
    def get(self, request, typeId):
        context = {'typeId': typeId}
        return render(request, 'ScenicType/scenicType_modify.html', context)


class ListView(BaseView):  # 后台景区类型列表
    def get(self, request):
        # 使用模板
        return render(request, 'ScenicType/scenicType_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        scenicTypes = ScenicType.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(scenicTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        scenicTypes_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        scenicTypeList = []
        for scenicType in scenicTypes_page:
            scenicType = scenicType.getJsonObj()
            scenicTypeList.append(scenicType)
        # 构造模板页面需要的参数
        scenicType_res = {
            'rows': scenicTypeList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(scenicType_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除景区类型信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        typeIds = self.getStrParam(request, 'typeIds')
        typeIds = typeIds.split(',')
        count = 0
        try:
            for typeId in typeIds:
                ScenicType.objects.get(typeId=typeId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出景区类型信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        scenicTypes = ScenicType.objects.all()
        #将查询结果集转换成列表
        scenicTypeList = []
        for scenicType in scenicTypes:
            scenicType = scenicType.getJsonObj()
            scenicTypeList.append(scenicType)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(scenicTypeList)
        # 设置要导入到excel的列
        columns_map = {
            'typeId': '类型id',
            'typeName': '类别名称',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'scenicTypes.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="scenicTypes.xlsx"'
        return response

