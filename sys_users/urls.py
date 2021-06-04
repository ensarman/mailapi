from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LoginView,
    CompanyView,
    RemoveDomain,
    RemoveUser,
    RemoveEmail,
    ListEmailByDomain,
    ListAliasByDomain,
    AddEmail,
    UpdateEmail
)

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('company/<int:company_id>', CompanyView.as_view(), name="company"),
    path('company/', CompanyView.as_view(), name="company"),
    path('remove_domain/<int:company_id>/<int:pk>',
         RemoveDomain.as_view(), name="remove_domain"),
    path('remove_user/<int:company_id>/<int:pk>',
         RemoveUser.as_view(), name="remove_user"),
    # path(
    #     'emails_by_domain/',
    #     ListEmailByDomain.as_view(),
    #     name="email_by_domain"
    # ),
    path(
        'emails_by_domain/<int:company_id>/',
        ListEmailByDomain.as_view(),
        name="email_by_domain"
    ),
    path(
        'emails_by_domain/<int:company_id>/<int:domain_id>',
        ListEmailByDomain.as_view(),
        name="email_by_domain"
    ),
    path(
        'alias_by_domain/<int:domain_id>/',
        ListAliasByDomain.as_view(),
        name="alias_by_domain"
    ),
    path(
        'alias_by_domain/<int:domain_id>/<str:source>',
        ListAliasByDomain.as_view(),
        name="alias_by_domain"
    ),
    path(
        'add_email/<int:company_id>/<int:domain_id>/',
        AddEmail.as_view(), name="add_email"
    ),
    path('update_email/<int:company_id>/<int:domain_id>/<int:pk>',
         UpdateEmail.as_view(), name="update_email"),
    path(
        'remove_email/<int:company_id>/<int:domain_id>/<int:pk>',
        RemoveEmail.as_view(), name='remove_email'
    ),
    #   path()
]
