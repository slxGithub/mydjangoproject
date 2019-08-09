from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from django.http import request,Http404
from django.views.generic import View
from django.contrib.auth import authenticate,login
# Create your views here.


from django.contrib.auth.backends import ModelBackend

from utils.send_email import send_register_eamil
from .models import UserProfile,EmailVerifyRecord
from django.db.models import Q
from .form import LoginForm,RegisterForm

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


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email',None)
            if UserProfile.objects.filter(email=email):
                return render(request,'register.html',{'register_form':register_form,'msg':'邮箱已被占用'})

            password = request.POST.get('password',None)

            userprofile = UserProfile()
            userprofile.username = email
            userprofile.email = email
            userprofile.is_active = True
            userprofile.password = make_password(password)
            userprofile.save()

            send_register_eamil(email,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            # 验证码不对的时候跳转到激活失败页面
        else:
            return render(request, 'active_fail.html')
            # 激活成功跳转到登录页面
        return render(request, "login.html", )



