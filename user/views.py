from hashlib import sha1

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *

# Create your views here.

'''
handle with the module of users
'''


def register(request):
    title = "注册"
    return render(request, 'user/register.html', locals())


def register_handler(request):
    post = request.POST
    uname = post['user_name']
    upwd = post['pwd']
    ucpwd = post['cpwd']
    uemail = post['email']
    uallow = post['allow']
    if upwd != ucpwd or upwd == ucpwd == "":
        return redirect(register)

    if UserInfo.objects.filter(uname__exact=uname):
        return redirect(register_exist)

    # 加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd2 = s1.hexdigest()
    UserInfo(uname=uname, upwd=upwd2, uemail=uemail).save()
    return redirect(login)


def register_exist(request):
    uname = request.GET['uname']
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    context = {'title': "登录", 'error_name': 0, 'error_pwd': 0,
               'uname': request.COOKIES.get('uname', ""), 'upwd': request.COOKIES.get("upwd", "")}
    return render(request, 'user/login.html', locals())


def login_handler(request):
    title = "用户中心"
    post = request.POST
    uname = post['username']
    upwd = post['pwd']
    ujizhu = post.get('jizhu', 0)

    if uname == "":
        return redirect(login)

    users = UserInfo.objects.filter(uname__exact=uname)
    if users:
        user = users[0]
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        upwd2 = s1.hexdigest()
        if upwd2 == user.upwd:
            r = redirect(info)
            if ujizhu != 0:
                r.set_cookie('uname', uname)
            else:
                r.set_cookie('uname', max_age=-1)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.uname
            return r;
        else:
            context = {'title': "登录", 'error_name': 0, 'error_pwd': 1,
                       'uname': uname, 'upwd': upwd}
            return render(request, 'user/login.html', context=context)
    else:
        context = {'title': "登录", 'error_name': 1, 'error_pwd': 0,
                   'uname': uname, 'upwd': upwd}
        return render(request, 'user/login.html', context=context)


def info(request):
    context = {
        'title': '用户中心',
        'user': UserInfo.objects.get(id=request.session['user_id'])
    }

    return render(request, 'user/user_center_info.html', context=context)