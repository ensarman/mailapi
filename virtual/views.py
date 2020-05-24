from django.views.generic import ListView, FormView, CreateView
from django.views.generic.list import BaseListView, MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import User
from .forms import UserForm

from django.http import HttpResponse

# Create your views here.


class ListUsers(LoginRequiredMixin, ListView, FormMixin):
    """Tiene el FormMixin pero tenemos que manejar nosotros el
     procesamiento del Form de otra forma es un dolor de trasero"""

    def __init__(self, *args, **kwargs):
        super(ListUsers, self).__init__(*args, **kwargs)
        self.success_url = reverse('mail:user_list')
        self.model = User
        self.paginate_by = 5
        self.ordering = '-id'
        self.form_class = UserForm
        self.object_list = self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserForm
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        context = super().get_context_data()
        context['form'] = form
        return self.render_to_response(context=context)

    def form_invalid(self, form):
        context = super().get_context_data()
        context['form'] = form
        return self.render_to_response(context=context)





