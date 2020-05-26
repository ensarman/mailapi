from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .models import Company

# Create your views here.

class LoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("mail:user_list")
    title = "Login Email Magnament"

class sysUsers(LoginRequiredMixin, ListView):
    pass

@method_decorator(staff_member_required, name='dispatch')
class CompanyView(LoginRequiredMixin, ListView):
    model = Company
    ordering = '-id'
    paginate_by = 5
    title = "Email Magnament"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        try:
            context['company'] = self.kwargs['comapany_id']
        except KeyError as e:
            pass

        return context


