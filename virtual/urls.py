from django.urls import path, reverse, reverse_lazy
from django.views.generic import DeleteView, CreateView, ListView
from .views import BaseList
from .models import User, Domain, Alias
from .forms import UserForm, DomainForm

urlpatterns = [
    path('users/', BaseList.as_view(
        model=User,
        form_class=UserForm,
        paginate_by=10,
        success_url=reverse_lazy('mail:user_list'),
        ordering='-id'
    ), name="user_list"),
    path(
        'domains/',
        BaseList.as_view(
            model=Domain,
            form_class=DomainForm,
            paginate_by=10,
            success_url=reverse_lazy('mail:domain_list'),
            ordering='-id'
        ),
        name="domain_list"),
    path(
        'create_domain/',
        CreateView.as_view(
            model=Domain,
            form_class=DomainForm),
        name='domain_create'
    ),
    path(
        'delete_user/<int:pk>', DeleteView.as_view(
            model=User,
            success_url=reverse_lazy('mail:user_list'),
        ), name='user_delete'
    ),
    path(
        'delete_domain/<int:pk>',
        DeleteView.as_view(
            model=Domain,
            success_url=reverse_lazy('mail:domain_list'),
        ), name='domain_delete'
    ),
]
