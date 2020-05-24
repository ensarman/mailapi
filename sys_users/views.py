from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME

from django.urls import reverse_lazy

# Create your views here.

class LoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("mail:user_list")
    title = "Login Email Magnament"

