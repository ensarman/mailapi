from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User

from django.http import HttpResponse

# Create your views here.

class ListUsers(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 5
    ordering = '-id'

