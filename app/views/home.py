from typing import Any
from django.views.generic import TemplateView
from globals.request_manager import Action
from frontend.settings import MAIN_URL

class home_view (TemplateView) : 
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        
        level = self.request.GET.get('level', None)
        context['current_level'] = 'all'

        if level is None :
            action = Action(
                url=MAIN_URL+'/exam/get/'
            )
        else:
            action = Action(
                url=MAIN_URL+'/exam/get/?level=' + level
            )
            context['current_level'] = level

        action.get()
        context['exams'] = action.json_data()
        
        # get levels
        action_levels = Action(
            url=MAIN_URL+'/levels/'
        )

        action_levels.get()
        context['levels'] = action_levels.json_data()
        
        return context
    