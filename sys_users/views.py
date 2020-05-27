from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .models import Company, DomainAdmin
from .forms import CreateUserForm
from virtual.forms import DomainForm

# Create your views here.

class LoginView(LoginView):
    template_name = "sys_users/login.html"
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
            context['company'] = Company.objects.get(id=self.kwargs['company_id'])
            context['domain_form'] = DomainForm
            context['user_form'] = CreateUserForm
            context['sys_user'] = DomainAdmin
        except KeyError as e:
            context['company'] = "---"


        return context


