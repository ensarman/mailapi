from django.contrib.auth.views import LoginView, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, DeleteView

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction

from .models import Company, DomainAdmin
from .forms import CreateUserForm
from virtual.forms import DomainForm
from virtual.models import Domain, User as Email


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
            """Si el formulario es de dominios"""
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
            """si el formulario es del usuarios"""
            form = CreateUserForm(self.request.POST)
            if form.is_valid():
                user = form.save()
                company = Company.objects.get(id=self.request.POST.get('company_id'))
                sys_user = DomainAdmin.objects.create(user=user)
                sys_user.company.add(company)
                return redirect('sys_users:company', self.request.POST.get('company_id'))
            else:
                self.object_list = self.get_queryset()
                context = self.get_context_data()
                context['user_form'] = form
                return self.render_to_response(context)


@method_decorator(staff_member_required, name='dispatch')
class RemoveDomain(LoginRequiredMixin, DeleteView):
    model = Domain

    def get_success_url(self):
        return reverse_lazy('sys_users:company', kwargs={'company_id': self.kwargs.get('company_id')})


@method_decorator(staff_member_required, name='dispatch')
class RemoveUser(LoginRequiredMixin, DeleteView):
    model = get_user_model()

    def get_success_url(self):
        return reverse_lazy('sys_users:company', kwargs={'company_id': self.kwargs.get('company_id')})


class ListEmailByDomain(LoginRequiredMixin, ListView):
    """Lista los emails por dominio, pero verificando la autenticacion,
     osea los dominios que le corresponden al usuario logueado"""
    title = "Email List By Domain"
    model = Email  # el queryset debe retornar los usuarios de emails
    paginate_by = 10
    companies = None
    domains = None
    template_name = 'sys_users/emails.html'

    def get_queryset(self):
        user = self.request.user.domainadmin
        self.companies = user.company.all()

        if self.kwargs.get('company_id'):
            """ Todos los dominios de la compañía seleccionada """
            if self.kwargs.get('domain_id'):
                """si es que hay domain_id en la url"""
                self.domains = user.company.all().get(id=self.kwargs.get('company_id')).domain.all().filter(id=self.kwargs.get('domain_id'))
            else:
                self.domains = user.company.all().get(id=self.kwargs.get('company_id')).domain.all()
            emails = Email.objects.none()
            for domain in self.domains:
                emails = emails | domain.user_set.all()
            return emails

        elif self.companies.__len__() == 1:
            """Cuando no hay company pero hay solo una"""
            self.domains = self.companies[0].domain.all()
            emails = Email.objects.none()
            for domain in self.domains:
                emails = emails | domain.user_set.all()
            return emails
        else:
            """cuando no hay ni company_id 
            ni solo tiene una compañia
            tiene que devolver todos los dominios del usuario
            """
            self.domains = Domain.objects.none()
            for company in self.companies:  # crear queryset de todos los dominios
                self.domains = self.domains | company.domain.all()

            emails = Email.objects.none()
            for company in self.companies:
                for domain in company.domain.all():
                    emails = emails | domain.user_set.all()

            return emails

    def get_context_data(self, *args, **kwargs):
        context = super(ListEmailByDomain, self).get_context_data(*args, **kwargs)
        context['companies'] = self.companies
        context['domains'] = self.domains
        context['emails'] = self.get_queryset  # Alias para los emails
        return context
