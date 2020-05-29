from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    LoginView,
    CompanyView,
    RemoveDomain,
    RemoveUser
)

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('company/<int:company_id>', CompanyView.as_view(), name="company"),
    path('company/', CompanyView.as_view(), name="company"),
    path('remove_domain/<int:company_id>/<int:pk>', RemoveDomain.as_view(), name="remove_domain"),
    path('remove_user/<int:company_id>/<int:pk>', RemoveUser.as_view(), name="remove_user")
]
