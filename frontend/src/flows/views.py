from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from .models import Flow
# Create your views here.
class FlowsView(LoginRequiredMixin, View):
    """
        Displays data related to Flows - if user is staff.
        
        :model:`flows.Flow`
        
        **Context**
        
        :model:`flows.Flow`
        
        ``flows``: a list of all Flow objects.
        
        **Template**
        
        :template:`dashboard/flows.html`
        
        """
    def get(self, request, *args, **kwargs):
        """ Takes request, renders page.
            """
        if request.user.is_staff:
            flows = Flow.objects.order_by('id')
        else:
            flows = None


        context = {
            'flows':flows
        }

        return render(request, 'dashboard/flows.html', context=context)
