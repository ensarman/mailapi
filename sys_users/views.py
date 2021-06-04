from django.contrib.auth.views import LoginView, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, DeleteView

from django.conf import settings
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db import transaction
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.views.generic.edit import CreateView, UpdateView

from .models import Company, DomainAdmin
from .forms import CompanyForm, CreateUserForm
from virtual.forms import DomainForm, UserForm as EmailForm
from virtual.models import Domain, Alias, User as Email

# Create your views here.


class LoginView(LoginView):
    """
    To login ;)
    """
    template_name = "sys_users/login.html"
    redirect_authenticated_user = True
    # success_url = reverse_lazy("mail:user_list")
    title = "Login Email Magnament"

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy("home")
        else:
            return reverse_lazy("sys_users:email_by_domain", kwargs={
                'company_id': self.request.user.domainadmin.company.first().id
            }
            )


class sysUsers(LoginRequiredMixin, ListView):
    pass


@method_decorator(staff_member_required, name='dispatch')
class CompanyView(LoginRequiredMixin, ListView):
    """
    ListView of all companies
    """
    model = Company
    ordering = '-id'
    paginate_by = 20
    title = "Email Magnament"
    company_form = CompanyForm
    domain_form = DomainForm
    user_form = CreateUserForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.title
        context['company_form'] = self.company_form
        try:
            context['company'] = Company.objects.get(
                id=self.kwargs['company_id'])
            context['domain_form'] = self.domain_form
            context['user_form'] = self.user_form
            context['sys_user'] = DomainAdmin
        except KeyError:
            context['company'] = "---"

        return context

    @transaction.atomic
    def post(self, *args, **kwargs):
        if self.request.POST.get('form') == 'domain':
            """Si el formulario es de dominios"""
            form = DomainForm(self.request.POST)
            if form.is_valid():
                domain = form.save()
                company = Company.objects.get(
                    id=self.request.POST.get('company_id'))
                company.domain.add(domain)
                return redirect('sys_users:company', self.request.POST.get('company_id'))
            else:
                self.object_list = self.get_queryset()
                context = self.get_context_data()
                context['domain_form'] = form
                return self.render_to_response(context)

        elif self.request.POST.get('form') == 'user':
            """si el formulario es del usuarios"""
            form = CreateUserForm(self.request.POST)
            if form.is_valid():
                user = form.save()
                company = Company.objects.get(
                    id=self.request.POST.get('company_id'))
                sys_user = DomainAdmin.objects.create(user=user)
                sys_user.company.add(company)
                return redirect('sys_users:company', self.request.POST.get('company_id'))
            else:
                self.object_list = self.get_queryset()
                context = self.get_context_data()
                context['user_form'] = form
                return self.render_to_response(context)
        elif self.request.POST.get('form') == 'company':
            """ si es que se ejecuta crear nueva comañia """
            form = CompanyForm(self.request.POST)
            if form.is_valid():
                company = form.save()
                if self.kwargs.get('company_id', False):
                    return redirect('sys_users:company', self.kwargs.get('company_id'))
                else:
                    return redirect('sys_users:company')

            else:
                self.object_list = self.get_queryset()
                context = self.get_context_data()
                context['company_form'] = form
                return self.render_to_response(context)


@method_decorator(staff_member_required, name='dispatch')
class RemoveDomain(LoginRequiredMixin, DeleteView):
    """
    Removes a domaain
    """
    model = Domain

    def get_success_url(self):
        return reverse_lazy('sys_users:company', kwargs={'company_id': self.kwargs.get('company_id')})


@method_decorator(staff_member_required, name='dispatch')
class RemoveUser(LoginRequiredMixin, DeleteView):
    """
    Removes a system user
    """
    model = get_user_model()

    def get_success_url(self):
        return reverse_lazy('sys_users:company', kwargs={'company_id': self.kwargs.get('company_id')})


class ListEmailByDomain(LoginRequiredMixin, ListView):
    """
    Lista los emails por dominio, pero verificando la autenticación,
    osea los dominios que le corresponden al usuario logueado
    """
    title = "Email List By Domain"
    model = Email  # el queryset debe retornar los usuarios de emails
    paginate_by = 10
    ordering = 'email'
    companies = None
    domains = None
    user = None
    template_name = 'sys_users/emails.html'
    email_form = EmailForm

    def __init__(self, *args, **kwargs):
        super(ListEmailByDomain, self).__init__()

    def get(self, *args, **kwargs):
        self.user = self.request.user.domainadmin
        self.companies = self.user.company.all()
        if self.companies.count() == 1:
            self.kwargs = {
                'company_id': self.companies[0].id,
                'domain_id': self.companies[0].domain.all()[0].id,
            }
        return super(ListEmailByDomain, self).get(*args, **kwargs)

    def get_queryset(self):
        if self.kwargs.get('company_id'):
            """ Todos los dominios de la compañía seleccionada """
            self.domains = self.user.company.all().get(
                id=self.kwargs.get('company_id')).domain.all()
            emails = Email.objects.none()
            for domain in self.domains:
                emails = emails | domain.user_set.all()

        elif self.companies.__len__() == 1:
            """Cuando no hay company pero hay solo una"""
            self.domains = self.companies[0].domain.all()
            emails = Email.objects.none()
            for domain in self.domains:
                emails = emails | domain.user_set.all()
        else:
            """cuando no hay ni company_id
            ni solo tiene una compañia
            tiene que devolver todos los dominios del usuario
            """
            self.domains = Domain.objects.none()
            for company in self.companies:  # crear queryset de todos los dominios
                self.domains = self.domains | company.domain.all()

            if self.kwargs.get('domain_id'):
                """esto esta muy hardcoded, hay que suavsarlo un poco"""
                self.domains = self.domains.filter(
                    id=self.kwargs.get('domain_id'))

            emails = Email.objects.none()
            for domain in self.domains:
                emails = emails | domain.user_set.all()

        # configurando el filtro para la búsqueda
        if self.request.GET.get('email'):
            emails = emails.filter(
                email__icontains=self.request.GET.get('email'))

        return emails.order_by('-id')

    def get_context_data(self, *args, **kwargs):
        current_domain = ""
        if self.kwargs.get('domain_id'):
            current_domain = self.domains.get(id=self.kwargs['domain_id'])

        context = super(ListEmailByDomain, self).get_context_data(
            *args, **kwargs)
        context['companies'] = self.companies
        context['domains'] = self.domains
        context['emails'] = self.get_queryset  # Alias para los emails
        context['current_domain'] = current_domain
        return context


class RemoveEmail(LoginRequiredMixin, DeleteView):
    model = Email

    def get_success_url(self):
        return reverse_lazy('sys_users:email_by_domain', kwargs={
            'company_id': self.kwargs.get('company_id'),
            'domain_id': self.kwargs.get('domain_id')
        })


class AddEmail(LoginRequiredMixin, CreateView):
    model = Email
    fields = ('domain', 'email', 'password', 'quota')

    def get_success_url(self):
        return reverse_lazy('sys_users:email_by_domain', kwargs={
            'company_id': self.kwargs.get('company_id'),
            'domain_id': self.kwargs.get('domain_id')
        })

    def post(self, request, *args, **kwargs):
        # self.object = None
        company_id = self.kwargs.get('company_id')

        form = self.get_form()

        company = Company.objects.get(id=company_id)
        response_json = {
            'status': 'unknown',
            'comment': 'unknown'
        }

        virtual_full = company.get_used_quota() + int(request.POST.get('quota')) * \
            settings.BYTE_TO_GIGABYTE_FACTOR > company.quota_total

        if company.is_full() or virtual_full:
            response_json['status'] = 'error'
            response_json['comment'] = 'company full'
        elif form.is_valid() and not virtual_full:
            object = form.save()
            response_json['status'] = 'success'
            response_json['comment'] = object.email

        if not form.is_valid():
            response_json['status'] = 'error'
            response_json['comment'] = 'bad data'

        return JsonResponse(response_json)


class UpdateEmail(LoginRequiredMixin, UpdateView):
    model = Email
    form_class = EmailForm

    def get_success_url(self):
        return reverse_lazy('sys_users:email_by_domain', kwargs={
            'company_id': self.kwargs.get('company_id'),
            'domain_id': self.kwargs.get('domain_id')
        })

    def post(self, request, *args, **kwargs):
        company_id = self.kwargs.get('company_id')

        self.object = self.get_object()
        form = self.get_form()

        company = Company.objects.get(id=company_id)
        response_json = {
            'status': 'unknown',
            'comment': 'unknown'
        }

        requested_quota = int(request.POST.get('quota')) * \
            settings.BYTE_TO_GIGABYTE_FACTOR

        increment = self.object.quota - requested_quota

        if self.object.quota < requested_quota:
            increment = abs(increment)
        else:
            increment = increment * -1

        virtual_full = company.get_used_quota() + increment > company.quota_total

        if (company.is_full() and increment >= 0) or virtual_full:
            response_json['status'] = 'error'
            response_json['comment'] = 'company full'
        elif form.is_valid() and not virtual_full:
            saved_email = form.save()
            response_json['status'] = 'success'
            response_json['comment'] = saved_email.email

        if not form.is_valid():
            response_json['status'] = 'error'
            response_json['comment'] = 'bad data'

        return JsonResponse(response_json)


def update_email(request):

    return redirect(
        reverse_lazy(
            'sys_users:email_by_domain',
            kwargs={
                'company_id': 0,
                'domain_id': 0,
            }
        )
    )


class ListAliasByDomain(LoginRequiredMixin, ListView):
    model = Alias
    template_name = "sys_users/alias.html"

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        aliases = self.model.objects.filter(
            domain=self.kwargs['domain_id'])

        # divide alias and forwards
        context['forwards'] = []
        context['groups'] = []

        for alias in aliases:
            if alias.source in alias.destination.split(','):
                context['forwards'] += [alias]
            else:
                context['groups'] += [alias]

        if self.kwargs.get('source'):
            context['destinations'] = self.model.objects.get(
                source=self.kwargs.get('source')
            ).destination.split(',')

        return context

    def get(self, request, *args, **kwargs):
        forbiden = True
        for company in request.user.domainadmin.company.all():
            if company.domain.all().filter(id=self.kwargs['domain_id']):
                forbiden = False

        if forbiden:
            return HttpResponseForbidden()
        else:
            return super().get(request, *args, **kwargs)
