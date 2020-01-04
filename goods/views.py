from django.shortcuts import render

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

