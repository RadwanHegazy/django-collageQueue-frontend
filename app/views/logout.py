from django.views import View
from django.shortcuts import redirect


class logout_view (View):
    def get(self, request):
        res = redirect('home')
        res.delete_cookie('user')
        return res