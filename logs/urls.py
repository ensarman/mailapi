from django.urls import path
from .views import BanLog


urlpatterns = [
    path('banlog', BanLog.as_view(), name="ban_log")
]
