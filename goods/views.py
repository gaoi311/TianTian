from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from .models import *

'''
handle with the good
'''


def index(request):
    typelist = TypeInfo.objects.all()
    type00 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('gclick')[0:3]

    type10 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('gclick')[0:3]

    type20 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('gclick')[0:3]

    type30 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('gclick')[0:3]

    type40 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('gclick')[0:3]

    type50 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('gclick')[0:3]

    context = {
        'title': '首页',
        'type00': type00, 'type01': type01,
        'type10': type10, 'type11': type11,
        'type20': type20, 'type21': type21,
        'type30': type30, 'type31': type31,
        'type40': type40, 'type41': type41,
        'type50': type50, 'type51': type51,
    }

    return render(request, 'goods/index.html', context=context)


def list(request, tid, pindex, sort):
    '''
    tid: 1-6
    pindex: current page
    sort: 1,default   2,price   3,hot
    :param request:
    :param tid:
    :param pindex:
    :param sort:
    :return:
    '''
    typelist = TypeInfo.objects.get(pk=int(tid))
    news = typelist.goodsinfo_set.order_by('-id')[0:2]
    goodslist = []
    if sort == 1:
        goodslist = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == 2:
        goodslist = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == 3:
        goodslist = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    paginator = Paginator(goodslist, 10)
    page = paginator.page(int(pindex))

    context = {
        'title': typelist.title,
        'page': page,
        'paginator': paginator,
        'pindex': pindex,
        'typeinfo': typelist,
        'sort': sort,
        'news': news
    }
    return render(request, 'goods/list.html', context=context)


def immedi_buy(request, gid, num):
    goods = GoodsInfo.objects.get(pk=int(gid))
    count = 1
    context = {
        'title': '提交订单',
        'count': count,
        'goods': goods,
        'num': num,
        'total': goods.gprice * int(num)
    }
    return render(request, 'goods/place_order.html', context=context)


def add_cart(request, gid, num):
    cart = request.session.get('cart', [])
    item = CartItem(gid, num)
    cart.append(item)
    request.session['cart'] = cart
    return render(request, 'goods/place_order.html')


def show_cart(request):
    cart = request.session.get('cart', [])
    context = {
        'title': '购物车',
        'cart': cart
    }
    return render(request, 'goods/cart.html', context=context)

