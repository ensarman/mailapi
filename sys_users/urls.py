from django.urls import path
from .views import LoginView, CompanyView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('company/<int:company_id>', CompanyView.as_view(), name="company"),
    path('company/', CompanyView.as_view(), name="company"),
]
