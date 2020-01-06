import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
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


def detail(request, gid):
    goods = GoodsInfo.objects.get(pk=int(gid))
    goods.gclick += 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    typeinfo = TypeInfo.objects.get(pk=goods.gtype_id)
    context = {
        'title': goods.gtype.title,
        'goods': goods,
        'news': news,
        'typeinfo': typeinfo,
        'gid': gid
    }
    return render(request, 'goods/detail.html', context=context)


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
    if sort == '1':
        goodslist = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':
        goodslist = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':
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
    return render(request, 'shop/place_order.html', context=context)


def show_cart(request):
    uid = request.session['user_id']
    cart = CartItem.objects.filter(user_id=uid)
    request.session['count'] = cart.count()
    total = 0
    for cartitem in cart:
        total += cartitem.num * cartitem.goods.gprice
    context = {
        'title': '购物车',
        'count': cart.count(),
        'cart': cart,
        'total': total
    }
    return render(request, 'goods/cart.html', context=context)


def add_cart(request, gid, num):
    gid = int(gid)
    num = int(num)
    uid = request.session['user_id']
    cart = CartItem.objects.filter(goods_id=gid, user_id=uid)
    # 先判断 该用户 购物车中 是否 存在 该商品
    # 如果纯在，则仅作数量上的 加法
    if len(cart) >= 1:
        cartitem = cart[0]
        cartitem.num += num
    else:
        cartitem = CartItem(user_id=uid, goods_id=gid, num=num)
    cartitem.save()
    # 判断请求方式 是否是ajax，若是则返回json格式的 商品数量即可
    if request.is_ajax():
        num = CartItem.objects.filter(user_id=uid).count()
        return JsonResponse({'num': num})
    else:
        return redirect(show_cart)


def delete_cart(request, id):
    id = int(id)
    CartItem.objects.get(pk=id).delete()
    return redirect(show_cart)
