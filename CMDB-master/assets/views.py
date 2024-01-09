from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from assets import models
from assets import asset_handler
from django.shortcuts import get_object_or_404


def index(request):
    """
    资产总表视图
    :param request:
    :return:
    """
    assets = models.CarDetail.objects.all()
    return render(request, 'assets/index.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/login/")

def dashboard(request):

    total = 974.4215
    upline = 400.6933
    offline = 37.5937
    breakdown = 49.1433
    backup = 80.9644
    unknown = 403.0268

    up_rate = round(upline/total*100)
    o_rate = round(offline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)

    server_number = 400.6933
    networkdevice_number = 37.5937
    storagedevice_number = 49.1433
    securitydevice_number = 80.9644
    software_number = 403.0268

    data_point1 = 707.8011
    data_point2 = 67.4509
    data_point3 = 549.4174
    data_point4 = 511.4561
    data_point5 = 517.2504
    data_point6 = 400.6933
    data_point7 = 525.7368529917002
    data_point8 = 28.5909
    data_point9 = 18.0632
    data_point10 = 27.5841
    data_point11 = 86.2701
    data_point12 = 106.9909
    data_point13 = 37.5937
    data_point14 = 52.367530994445086
    data_point15 = 93.6271
    data_point16 = 77.7454
    data_point17 = 49.3141
    data_point18 = 59.7801
    data_point19 = 58.6122
    data_point20 = 49.1433
    data_point21 = 40.359322853408754
    data_point22 = 65.5337
    data_point23 = 65.8892
    data_point24 = 67.9619
    data_point25 = 67.4328
    data_point26 = 92.3904
    data_point27 = 80.9644
    data_point28 = 80.22391111564636
    data_point29 = 28.1050
    data_point30 = 62.1570
    data_point31 = 103.9451
    data_point32 = 282.5171
    data_point33 = 535.9235
    data_point34 = 403.0268
    data_point35 = 1268.8171115173817

    return render(request, 'assets/dashboard.html', locals())


def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """

    asset = get_object_or_404(models.CarDetail, id=asset_id)
    inform = get_object_or_404(models.CarInfo, id=asset_id-1)
    return render(request, 'assets/detail.html', locals())





@csrf_exempt
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse('没有数据！')
        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须为字典格式！')
        # 你的检测代码

        sn = data.get('sn', None)

        if sn:
            asset_obj = models.Asset.objects.filter(sn=sn)  # [obj]
            if asset_obj:
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse('资产数据已经更新。')
            else:
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse('没有资产sn，请检查数据内容！')

    return HttpResponse('200 ok')
