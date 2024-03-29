from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, DeleteView

from django.conf import settings
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView

from .models import Company, DomainAdmin
from .forms import CompanyForm, CreateUserForm
from virtual.forms import DomainForm, UserForm as EmailForm
from virtual.models import Domain, Alias, User as Email

from accounts.views import LoginView

# Create your views here.


class LoginView(LoginView):
    """
    To login ;)
    """
    #template_name = "sys_users/login.html"
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
            """ si es que se ejecuta crear nueva compañia """
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

        elif self.request.POST.get('form') == 'company_quota':
            """ si se llama al formulario para quota total"""

            company = Company.objects.get(pk=self.kwargs.get('company_id'))
            quota_total = int(self.request.POST.get('quota_total'))
            company.quota_total = quota_total
            company.save()

            return redirect('sys_users:company', self.kwargs.get('company_id'))


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
                context['forwards'] += [alias.source]
            else:
                context['groups'] += [alias.source]

        if self.kwargs.get('source'):
            source = self.kwargs.get('source')
            try:
                alias = self.model.objects.get(
                    source=source
                )
                context['alias'] = alias
                context['source'] = source
                context['destinations'] = alias.destination.split(',')

                if source in context['forwards']:
                    context['is_forward'] = True
                elif source in context['groups']:
                    context['is_group'] = True
            except Exception as e:
                context['error'] = {
                    'error': e,
                    'message': "the address does not exists"
                }

        context['current_domain'] = Domain.objects.get(
            id=self.kwargs['domain_id'])

        context['emails'] = Email.objects.filter(
            domain_id=self.kwargs['domain_id'])

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


class AddSourceAlias(LoginRequiredMixin, CreateView):
    model = Alias
    fields = ("source", 'domain')

    @transaction.atomic
    def post(self, request):
        comapnies = request.user.domainadmin.company.all()
        allowed_domains = []
        for company in comapnies:
            for domain in company.domain.all():
                allowed_domains.append(domain)

        request_domain = Domain.objects.get(
            id=request.POST.get('domain'))

        response_json = {
            'status': 'unknown',
            'comment': 'unknown'
        }

        if (request_domain and request_domain in allowed_domains):
            # request.POST['domain'] = request.POST.get('domain_id')
            form = self.get_form()
            if form.is_valid():
                object = form.save()

                if request.POST.get('type') == 'forward':
                    object.destination = object.source
                    object.save()

                response_json['status'] = 'success'
                response_json['comment'] = object.source
            else:
                response_json['status'] = 'error'
                response_json['comment'] = form.errors
        else:
            response_json['status'] = 'error'
            response_json['comment'] = 'bad domain or not allowed'

        return (JsonResponse(response_json))


class RemoveAlias(LoginRequiredMixin, DeleteView):
    model = Alias

    def get_success_url(self):
        return reverse_lazy('sys_users:alias_by_domain', kwargs={
            'domain_id': self.kwargs.get('domain_id')
        })


class AddDestAlias(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, pk):
        # pk = self.kwargs.get('pk')
        destination = request.POST.get('destination')
        alias = Alias.objects.get(pk=pk)
        prev_dest = alias.destination.split(",")
        response_json = {
            "status": "",
            "comment": ""
        }

        if destination in prev_dest:
            response_json['status'] = 'error'
            response_json['comment'] = 'destination already set'
        else:
            prev_dest.append(destination)
            new_dest = ','.join(prev_dest)
            try:
                alias.destination = new_dest
                alias.save()
                response_json['status'] = "success"
                response_json['comment'] = alias.destination
            except Exception as e:
                response_json['status'] = "error"
                response_json['comment'] = "can't sava"
                response_json['exeception'] = e.__str__()

        return JsonResponse(response_json)


class RemoveDestAlias(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request, pk):
        destination = request.POST.get('destination')
        alias = Alias.objects.get(pk=pk)
        response_json = {
            'status': '',
            'comment': ''
        }

        dest = alias.destination.split(",")
        try:
            dest.remove(destination)
            try:
                alias.destination = ','.join(dest)
                alias.save()
                response_json['status'] = "success"
                response_json['comment'] = alias.destination
            except Exception as e:
                response_json['status'] = "error"
                response_json['comment'] = "can't save"
                response_json['exeception'] = e.__str__()
        except ValueError as e:
            response_json['status'] = "error"
            response_json['comment'] = f"the e-mail {destination} doesn't exist"
            response_json['exeception'] = e.__str__()

        return JsonResponse(response_json)


class GetEmails(LoginRequiredMixin, View):

    def post(self, request):
        domain_id = request.POST.get('domain_id')
        emails = Email.objects.filter(
            domain_id=domain_id).values('email')

        emails = tuple(emails)

        # emails_serialized = serializers.serialize('json', emails)
        # return HttpResponse(emails_serialized, content_type="application/json")
        return JsonResponse(emails, safe=False)
