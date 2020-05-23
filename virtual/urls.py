from django.urls import path
from .views import ListUsers

urlpatterns = [
    path('users', ListUsers.as_view(), name="user_list"),
]
