from django.contrib import admin
from .models import Domain

# Register your models here.


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", 'get_companies')
