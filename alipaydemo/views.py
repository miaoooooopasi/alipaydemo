from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from alipay import AliPay
import time
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt    # 取消 csrf组件
from .models import PayInfo, OrderInfo

from .tasks import test


def aliPay():
    obj = AliPay(
        appid=settings.APPID,
        app_notify_url=settings.NOTIFY_URL,  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成）
        alipay_public_key_path=settings.PUB_KEY_PATH,  # 支付宝公钥
        app_private_key_path=settings.PRI_KEY_PATH,  # 应用私钥
        debug=True,  # 默认False,
    )
    return obj


def index(request):
    if request.method == 'GET':
        # print(OrderInfo.objects.all())
        return render(request, 'alipaydemo/buy.html')

    alipay = aliPay()

    # 对购买的数据进行加密
    money = float(request.POST.get('price'))
    out_trade_no = "GGBOY" + str(time.time())
    # 1. 在数据库创建一条数据：状态（待支付）

    query_params = alipay.api_alipay_trade_page_pay(
        subject="test",  # 商品简单描述
        out_trade_no=out_trade_no,  # 商户订单号
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
        return_url='http://127.0.0.1:8000/alipaydemo/back_url',  # 支付成功后 - 重定向自己的网站
        notify_url='http://127.0.0.1:8000/alipaydemo/update_order'  # 支付成功后 - 发送的POST订单验证消息

    )

    # print(query_params)
    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

    return redirect(pay_url)


def back_url(request):
    """
     # 支付成功后的回调函数 -- 重定向自己的网站
　　　# 同时在重定向之前会校验此次支付信息是否正确
    :param request:
    :return:
    """

    params = request.GET.dict()
    sign = params.pop('sign', None)
    print('PARAMS', params)
    # print('sign', sign)
    alipay = aliPay()
    status = alipay.verify(params, sign)  # 返回 True or False
    print(status)
    if status:
        # 测试在数据库保存支付信息
        order = OrderInfo.objects.create(create_time='2019-07-22', money='12')
        order.save()
        print(order)
        # 这步是测试异步功能（函数是test）
        test.delay(1, 2)
        return HttpResponse('支付成功1')
    return HttpResponse('支付失败1')


@csrf_exempt
def update_order(request):
    """
    支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
    :param request:
    :return:
    """
    if request.method == 'POST':
        from urllib.parse import parse_qs

        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        print(post_dict)
        alipay = aliPay()

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
            # 修改订单状态
            out_trade_no = post_dict.get('out_trade_no')
            print('1111', out_trade_no)
            # 2. 根据订单号将数据库中的数据进行更新
            return HttpResponse('支付成功2')
        else:
            return HttpResponse('支付失败2')
    return HttpResponse('')
