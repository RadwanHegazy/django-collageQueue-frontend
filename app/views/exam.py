from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse, Http404
from django.views.generic import TemplateView
from django.shortcuts import render
from frontend.settings import MAIN_URL
from globals.request_manager import Action
from globals.decorators import login_required
from django.shortcuts import redirect

class exam_view (TemplateView) : 
    template_name = 'view_exam.html'
    
    @login_required
    def get(self, request: HttpRequest, exam_id, **kwargs) -> HttpResponse:
        headers = kwargs.get('headers', None)
        pending = request.GET.get('enter', None)
        done = request.GET.get('done', None)

        if headers != None and pending != None:
            section_id = pending
            self.make_pending(section_id, headers)
            return redirect('exam', exam_id)
        
        if headers != None and done != None :
            section_id = done
            self.make_done(section_id, headers)
            return redirect('exam', exam_id)

        action = Action(
            url=MAIN_URL+f'/exam/get/{exam_id}/',
        )
        action.get()

        if not action.is_valid:
            raise Http404(request)
        
        context = action.json_data()
        return render(request, self.template_name, context)
    

    @staticmethod
    def make_pending(section_id, headers) : 
        action = Action(
            url=MAIN_URL+f'/exam/section/pending/{section_id}/',
            headers=headers
        )
        action.patch()

    @staticmethod
    def make_done(section_id, headers) : 
        action = Action(
            url=MAIN_URL+f'/exam/section/done/{section_id}/',
            headers=headers
        )
        action.patch()


