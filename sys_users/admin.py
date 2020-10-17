from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import DomainAdmin, Company
from virtual.models import Domain
# from virtual.admin import DomainInline


class DomainInline(admin.StackedInline):
    model = Company.domain.through
    extra = 1


class DomainAdminInline(admin.StackedInline):
    model = DomainAdmin
    can_delete = False
    verbose_name_plural = 'Domain Admins'


class SysUser(BaseUserAdmin):
    inlines = (DomainAdminInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # inlines = (DomainInline,)
    list_display = ('name', 'id_number', 'get_domains')
    filter_horizontal = ('domain',)
    save_on_top = True


admin.site.unregister(User)
admin.site.register(User, SysUser)
