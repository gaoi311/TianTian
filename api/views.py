from django.core.mail.backends import console
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Payment1
from goods.models import GoodsInfo
from utils.pay import AliPay
import time
from django.conf import settings


def aliPay():
    obj = AliPay(
        appid=settings.APPID,
        app_notify_url=settings.NOTIFY_URL,  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成）
        return_url=settings.RETURN_URL,  # 如果支付成功，重定向回到你的网站的地址。
        alipay_public_key_path=settings.PUB_KEY_PATH,  # 支付宝公钥
        app_private_key_path=settings.PRI_KEY_PATH,  # 应用私钥
        debug=True,  # 默认False,
    )
    return obj


def index_many(request):
    print("index")
    if request.method == 'GET':
        return render(request, 'pay.html')

    alipay = aliPay()

    # 对购买的数据进行加密
    money = float(request.POST.get('price'))
    out_trade_no = "x2" + str(time.time())
    # 1. 在数据库创建一条数据：状态（待支付）

    ''' # 将付款记录写入数据库
        order_id = data.get("out_trade_no")     # 订单编号
        trade_id = data.get("trade_no")         # 交易流水号Payment1.objects.create(
        order_id=order_id,
        trade_id=trade_id,
    )'''

    query_params = alipay.direct_pay(
        subject="苹果",  # 商品简单描述
        out_trade_no=out_trade_no,  # 商户订单号
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
    )
    print(out_trade_no, 'test1')

    # 将待付款记录写入数据库
    # Payment1.objects.create(
    #     name='苹果',
    #     order_id=out_trade_no,
    #     trade_id='',
    #     total_amount=money,
    #     app_id='',
    #     seller_id='',
    #     timestamp='',
    # )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
    return redirect(pay_url)


def index_one(request, uid, gid, num):
    print("index")
    gid = int(gid)
    num = int(num)
    # if request.method == 'GET':
    #     return render(request, 'pay.html')

    alipay = aliPay()
    goods = GoodsInfo.objects.get(id=gid)
    request.session['gid'] = gid
    request.session['gtitle'] = goods.gtitle
    request.session['num'] = num
    total = goods.gprice * num

    # 对购买的数据进行加密
    money = float(total)
    out_trade_no = "x2" + str(time.time())
    # 1. 在数据库创建一条数据：状态（待支付）

    ''' # 将付款记录写入数据库
        order_id = data.get("out_trade_no")     # 订单编号
        trade_id = data.get("trade_no")         # 交易流水号Payment1.objects.create(
        order_id=order_id,
        trade_id=trade_id,
    )'''

    query_params = alipay.direct_pay(
        subject=goods.gtitle,  # 商品简单描述
        out_trade_no=out_trade_no,  # 商户订单号
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
    )
    print(out_trade_no, 'test1')

    # 将待付款记录写入数据库
    Payment1.objects.create(
        name=goods.gtitle,
        order_id=out_trade_no,
        trade_id='',
        total_amount=money,
        app_id='',
        seller_id='',
        timestamp='',
    )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
    return redirect(pay_url)


def pay_result(request):
    print("pay_result")
    """
    支付完成后，跳转回的地址
    :param request:
    :return:
    """
    params = request.GET.dict()
    sign = params.pop('sign', None)

    alipay = aliPay()
    # 校验支付是否成功
    status = alipay.verify(params, sign)

    order_id = params.get("out_trade_no")  # 订单编号
    trade_id = params.get("trade_no")  # 交易流水号Payment1.objects.create(
    total_amount = params.get('total_amount')  # 订单金额
    app_id = params.get('app_id')  # APPID
    seller_id = params.get('seller_id')  # 商户id
    timestamp = params.get('timestamp')  # 时间戳
    print(order_id, trade_id)
    print(order_id, 'test')

    if status:
        goods = GoodsInfo.objects.get(id=request.session['gid'])
        # return HttpResponse('成功')
        context = {
            'title': '我的订单',
            'flag': 1,
            'goods': goods,
            'num': request.session['num'],
            'order_id': order_id,
            'trade_id': trade_id,
            'total_amount': total_amount,
            'timestamp': timestamp
        }
        # 将付款记录写入数据库
        payment1 = Payment1.objects.get(order_id=order_id)
        payment1.order_id = order_id
        payment1.trade_id = trade_id
        payment1.total_amount = total_amount
        payment1.app_id = app_id
        payment1.seller_id = seller_id
        payment1.timestamp = timestamp
        payment1.save()
        return render(request, 'user/user_center_order.html', context=context)
    return HttpResponse('失败')


@csrf_exempt
def update_order(request):
    # 预留位置
    ''''''