from django.shortcuts import render
from django.http import request,Http404
from django.views.generic import View
from django.contrib.auth import authenticate,login
# Create your views here.


from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q
from .form import LoginForm

#邮箱和用户名都可以登录
# 基础ModelBackend类，因为它有authenticate方法
# class CustomBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
#             user = UserProfile.objects.get(Q(username=username)|Q(email=username))
#
#             # django的后台中密码加密：所以不能password==password
#             # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None

# 自定义后端
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    def get(self,request):
        return render(request,'login.html')

    def post(self,request):

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not all([username,password]):
                return render(request, 'login.html', {'msg': '参数不完整'})

            user = authenticate(username=username,password=password)
            if user:
                # 登录
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误','login_form':login_form})
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误','login_form':login_form})
