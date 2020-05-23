from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME

from django.urls import reverse_lazy

# Create your views here.

class LoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("mail:user_list")
    # redirect_field_name = REDIRECT_FIELD_NAME

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['login'] = True
        return context

    # def form_vaild(self, form):
    #     login(self.request, form.get_user())
    #
    #     if self.request.session.test_cookie_worked():
    #         self.request.session.delete_test_cookie()
    #
    #     return super(LoginView, self).form_valid(form)

    # def get_success_url(self):
    #     return self.success_url

