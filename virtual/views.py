from django.views.generic import ListView, DeleteView
from django.views.generic.list import BaseListView, MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse

# Create your views here.


class BaseList(LoginRequiredMixin, ListView, FormMixin):
    """Tiene el FormMixin pero tenemos que manejar nosotros el
     procesamiento del Form de otra forma es un dolor de trasero"""

    title = "Email Magnament"

    def __init__(self, *args, **kwargs):
        super(BaseList, self).__init__(*args, **kwargs)
        self.object_list = self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        context = super().get_context_data()
        form.save()
        context['form'] = form
        return self.render_to_response(context=context)

    def form_invalid(self, form):
        context = super().get_context_data()
        context['form'] = form
        return self.render_to_response(context=context)



