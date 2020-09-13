from django.views.generic import ListView, UpdateView, DetailView, View
from django.views.generic.detail import BaseDetailView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict

import json

from .models import User, Domain

# Create your views here.


@method_decorator(staff_member_required, name='dispatch')
class BaseList(LoginRequiredMixin, ListView, FormMixin):
    """Tiene el FormMixin pero tenemos que manejar nosotros el
     procesamiento del Form de otra forma es un dolor de trasero"""


    title = "Email Magnament"

    def __init__(self, *args, **kwargs):
        super(BaseList, self).__init__(*args, **kwargs)

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
        form.save()
        return redirect('virtual:user_list')

    def form_invalid(self, form):
        self.object_list = self.get_queryset()
        context = super().get_context_data()
        context['form'] = form
        return self.render_to_response(context=context)




def user_detail_json(request, pk):
    user = User.objects.get(id=pk)

    dict ={
        'email': user.email,
        'domain': user.email.__str__(),
        'quota': user.quota,
    }
    #dict = model_to_dict(user)
    #del dict['password']

    return HttpResponse(json.dumps(dict), content_type='application/json')

