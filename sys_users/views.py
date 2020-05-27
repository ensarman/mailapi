from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, FormView, CreateView

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import redirect
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
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.title
        try:
            context['company'] = Company.objects.get(id=self.kwargs['company_id'])
            context['domain_form'] = self.domain_form
            context['user_form'] = self.user_form
            context['sys_user'] = DomainAdmin
        except KeyError as e:
            context['company'] = "---"

        return context

    @transaction.atomic
    def post(self, *args, **kwargs):
        if self.request.POST.get('form') == 'domain':
            form = DomainForm(self.request.POST)
            if form.is_valid():
                domain = form.save()
                company = Company.objects.get(id=self.request.POST.get('company_id'))
                company.domain.add(domain)
                return redirect('sys_users:company', self.request.POST.get('company_id'))
            else:
                self.object_list = self.get_queryset()
                context = self.get_context_data()
                context['domain_form'] = form
                return self.render_to_response(context)
        if self.request.POST.get('form') == 'user':
            pass

