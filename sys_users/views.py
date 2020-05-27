from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, FormView

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.db import transaction

from .models import Company, DomainAdmin
from .forms import CreateUserForm
from virtual.forms import DomainForm
from virtual.models import Domain

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
    domain_form = DomainForm
    user_form = CreateUserForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        try:
            context['company'] = Company.objects.get(id=self.kwargs['company_id'])
            context['domain_form'] = self.domain_form
            context['user_form'] = self.user_form
            context['sys_user'] = DomainAdmin
        except KeyError as e:
            context['company'] = "---"


        return context


@method_decorator(staff_member_required, name='dispatch')
class CreateDomainView(LoginRequiredMixin, FormView):
    form_class = DomainForm
    #success_url = reverse_lazy('sys_users:company')

    @transaction.atomic
    def form_valid(self, form):
        domain = form.save()
        company = Company.objects.get(id=self.request.POST.get('company_id'))
        company.domain.add(domain)
        return super().form_valid(form)

    def form_invalid(self, form):


    def get_success_url(self, **kwargs):
        return reverse_lazy('sys_users:company', kwargs={'company_id': self.request.POST.get('company_id')})




