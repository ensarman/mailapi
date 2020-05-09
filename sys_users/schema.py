from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from .models import DomainAdmin, Business
from django.db import transaction

class SysUserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class DomainAdminType(DjangoObjectType):
    class Meta:
        model = DomainAdmin
class BusinessType(DomainAdminType):
    class Meta:
        model = Business

class CreateSysUser(graphene.Mutation):
    user = graphene.Field(SysUserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        return CreateSysUser(user=user)

class CreateDomainAdmin(graphene.Mutation):
    domain_admin = graphene.Field(DomainAdminType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        domain = graphene.Int()
        business = graphene.Int(required=True)

    def mutate(self, info, username, password, email, domain, business):
        with transaction.atomic():
            user = get_user_model()(
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()

            domain_admin = DomainAdmin.objects.create(
                user=user,
                business_id=business
            )
            if domain_admin is not None:
                domain_admin.domain.add(domain)

            return CreateDomainAdmin(domain_admin=domain_admin)


class Query(graphene.ObjectType):
    me = graphene.Field(SysUserType)
    all_sys_users = graphene.List(SysUserType)
    sys_user = graphene.Field(SysUserType)
    all_domain_admins = graphene.List(DomainAdminType)
    all_business = graphene.List(BusinessType)

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!!!")
        return user

    def resolve_all_sys_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_sys_user(self, info, sys_user, **kwargs):
        return get_user_model().objects.get(id=sys_user)

    def resolve_all_domain_admins(self, info, **kwargs):
        return DomainAdmin.objects.all()

    def resolve_all_business(self, info, **kwargs):
        return Business.objects.all()

class Mutation(graphene.ObjectType):
    create_sys_user = CreateSysUser.Field()
    create_domain_admin = CreateDomainAdmin.Field()
