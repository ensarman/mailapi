from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings


# Create your views here.


class ResetPassword(auth_views.PasswordResetView):
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    from_email = settings.EMAIL_HOST_USER


class ResetPasswordDone(auth_views.PasswordResetDoneView):
    template_name = "password_reset_sent.html"


class ResetPasswordConfirm(auth_views.PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class ResetPasswordComplete(auth_views.PasswordResetCompleteView):
    template_name = "password_reset_complete.html"
