from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ResetPassword,
    ResetPasswordDone,
    ResetPasswordConfirm,
    ResetPasswordComplete,
    LoginView
)

urlpatterns = [
    path('reset_password/', ResetPassword.as_view(), name="reset_password"),
    path('reset_password_sent/', ResetPasswordDone.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirm.as_view(),
         name="password_reset_comfirm"),
    path('reset_password_complete/', ResetPasswordComplete.as_view(),
         name="password_reset_complete"),
    path('login', LoginView.as_view(), name="login")
]
