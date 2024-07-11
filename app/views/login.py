from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect
from globals.request_manager import Action
from frontend.settings import MAIN_URL
from django.contrib import messages

class login_view (TemplateView) :
    template_name = 'login.html'

    def post (self, request) : 
        data = {
            'email' : request.POST.get('email', None),
            'password' : request.POST.get('password', None),
        }
        action = Action(
            url=MAIN_URL+'/user/auth/login/',
            data=data
        )
        action.post(),
        print(action.json_data())

        if not action.is_valid:
            messages.error(request, 'البيانات غير صحيحة')
            return redirect('login') 
        
        user_token = action.json_data()['access_token']
        response = redirect('home')
        response.set_cookie('user', user_token)
        messages.success(request,'تم تسجيل الدخول بنجاح')
        return response