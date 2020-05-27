from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import DomainAdmin, Company


class DomainAdminInline(admin.StackedInline):
    model = DomainAdmin
    can_delete = False
    verbose_name_plural = 'Domain Admins'


class SysUser(BaseUserAdmin):
    inlines = (DomainAdminInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, SysUser)
