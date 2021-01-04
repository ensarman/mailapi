from django.contrib import admin
from .models import Domain, User as Email

# Register your models here.


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", 'get_companies')


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'quota')
