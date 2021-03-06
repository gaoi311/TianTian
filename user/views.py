import http
import random
import urllib
from hashlib import sha1

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from goods.models import *

# Create your views here.

'''
handle with the module of users
'''


def register(request):
    '''
    method: get, return a html
    :param request:
    :return:
    '''
    title = "注册"
    return render(request, 'user/register.html', locals())


# def register_handler(request):
#     '''
#     function of handling with register
#     :param request:
#     :return:
#     '''
#     post = request.POST
#     uname = post['user_name']
#     upwd = post['pwd']
#     ucpwd = post['cpwd']
#     uemail = post['email']
#     uallow = post['allow']
#     if upwd != ucpwd or upwd == ucpwd == "":
#         return redirect(register)
#
#     if UserInfo.objects.filter(uname__exact=uname):
#         return redirect(register_exist)
#
#     # 加密
#     s1 = sha1()
#     s1.update(upwd.encode('utf-8'))
#     upwd2 = s1.hexdigest()
#     UserInfo(uname=uname, upwd=upwd2, uemail=uemail).save()
#     return redirect(login)


def register_exist(request):
    '''
    function of handling with register when the user already exists
    :param request:
    :return:
    '''
    uname = request.GET['uname']
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    '''
    method: get, return a html
    :param request:
    :return:
    '''
    context = {
        'title': "登录",
        'error_name': 0,
        'error_pwd': 0,
        'uname': request.COOKIES.get('uname', ""),
        'upwd': request.COOKIES.get("upwd", "")
    }
    return render(request, 'user/login.html', locals())


def login_handler(request):
    '''
    function of handling with login
    :param request:
    :return:
    '''
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
        print('111')
        if upwd2 == user.upwd:
            print('222')
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


def register_handler(request):
    user_name = request.POST.get('user_name')
    users = UserInfo.objects.filter(uname__exact=user_name)
    if len(users) > 0:
        return redirect(register)

    pwd = request.POST.get('pwd')
    cpwd = request.POST.get('cpwd')
    phone = request.POST.get('mobile')
    email = request.POST.get('email')

    if pwd != cpwd:
        return redirect(register)

    s1 = sha1()
    s1.update(pwd.encode('utf-8'))
    cpwd = s1.hexdigest()

    user_info = UserInfo()
    user_info.uname = user_name
    user_info.upwd = cpwd
    user_info.uphone = phone
    user_info.umail = email
    user_info.save()
    return redirect(login)


def forget_pwd(request):
    return render(request, 'user/forget_pwd.html', context={'phone': "", 'title': '找回密码'})


def send_code(request):
    message_code = ''
    phone = request.POST.get('mobile')
    request.session['phone'] = phone

    for i in range(6):
        i = random.randint(0, 9)
        message_code += str(i)

    print("forget_handler" + message_code)
    request.session['message_code'] = message_code

    text = "您的验证码是：%s。请不要把验证码泄露给其他人。" % message_code

    # 用户名是登录用户中心->验证码短信->产品总览->APIID
    account = "C41333402"
    # 密码 查看密码请登录用户中心->验证码短信->产品总览->APIKEY
    password = "931590da0f3ee7cd5b91d893f468f046"
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"

    params = urllib.parse.urlencode({
            'account': account,
            'password': password,
            'content': text,
            'mobile': phone,
            'format': 'json'
        })
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()

    print(eval(response_str.decode()))
    # 使用eval把字符串转为json数据返回
    return render(request, 'user/forget_pwd.html', context={'phone': phone})


def update_pwd(request):
    message_code = request.session.get('message_code')
    print('Update_pwd' + message_code)
    code = request.POST.get('code')
    # name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    cpwd = request.POST.get('cpwd')
    if code != message_code:
        return redirect(forget_pwd)

    s1 = sha1()
    s1.update(pwd.encode('utf-8'))
    cpwd = s1.hexdigest()

    users = UserInfo.objects.filter(uphone__exact=request.session['phone'])
    if len(users) == 1:
        user = users[0]
        user.upwd = cpwd
        user.save()
        return redirect(login)

    return redirect(forget_pwd)


def info(request):
    '''
    function of handling with the user information
    :param request:
    :return:
    '''
    try:
        cart = CartItem.objects.filter(user_id=request.session['user_id'])
        request.session['count'] = cart.count()
        context = {
            'title': '用户中心',
            'user': UserInfo.objects.get(id=request.session['user_id'])
        }
        return render(request, 'user/user_center_info.html', context=context)
    except:
        alert = 1
        return render(request, 'user/login.html', locals())


def order(request):
    '''
    function of handling with the order
    :param request:
    :return:
    '''
    context = {
        'title': '用户中心',
    }
    return render(request, 'user/user_center_order.html', context=context)


def site(request):
    '''
    function of handling with the address of user
    :param request:
    :return:
    '''
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post['ushou']
        user.uaddress = post['uaddress']
        user.uyoubian = post['uyoubian']
        user.uphone = post['uphone']
        user.save()

    context = {
        'title': '用户中心',
        'user': user
    }

    return render(request, 'user/user_center_site.html', context=context)


def surprise_view(request):
    return render(request, 'surprise/spage.html')
