import graphene
from graphene_django import DjangoObjectType

from .models import Domain, User, Alias


class DomainType(DjangoObjectType):
    """
    Tipo para los Dominios
    """
    class Meta:
        model = Domain


class UserType(DjangoObjectType):
    """
    Tipo para cada Email
    """
    class Meta:
        model = User


class AliasType(DjangoObjectType):
    """
    Tipo para los Alias y redirecciones
    """
    class Meta:
        model = Alias


class CreateDomain(graphene.Mutation):
    """
    Mutation para crear un nuevo dominio
    """
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        domain = Domain(name=name)
        domain.save()

        return CreateDomain(
            id=domain.id,
            name=domain.name
        )

class CreateUser(graphene.Mutation):
    """
    Mutation para crear un nuevo E-Mail
    """
    id = graphene.Int()
    domain = graphene.Int()
    email = graphene.String()
    password = graphene.String()
    quota = graphene.Int()

    class Arguments:
        domain = graphene.Int()
        email = graphene.String()
        password = graphene.String()
        quota = graphene.Int()

    def mutate(self, info, domain, email, password, quota):
        user = User.objects.create(
            domain_id=domain,
            email=email,
            password=password,
            quota=quota
        )

        return CreateUser(
            id=user.id,
            email=user.email,
            password=user.password,
            quota=user.quota
        )

class DeleteUser(graphene.Mutation):
    """
    Mutation para eliminar un Usuario
    """
    id = graphene.Int()
    email = graphene.String()

    class Arguments:
        id = graphene.ID()

    user = graphene.Field(UserType)

    def mutate(self, info, id):
        user = User.objects.get(id=id)
        email = user.email
        user.delete()

        return DeleteUser(id=id, email=email)


class Query(graphene.ObjectType):
    domain = graphene.Field(
        DomainType,
        id=graphene.Int(),
        name=graphene.String()
    )
    all_domains = graphene.List(DomainType)
    user = graphene.Field(
        UserType,
        id=graphene.Int(),
        email=graphene.String()
    )
    all_users = graphene.List(UserType)
    all_aliases = graphene.List(AliasType)

    def resolve_domain(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Domain.objects.get(id=id)
        if name is not None:
            return Domain.objects.get(name=name)

    def resolve_all_domains(self, info, **kwargs):
        return Domain.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        email = kwargs.get('email')

        if id is not None:
            return User.objects.get(id=id)
        if email is not None:
            return User.objects.get(email=email)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.select_related('domain').all().order_by("-id")

    def resolve_all_aliases(self, info, **kwargs):
        return Alias.objects.select_related('domain').all()


class Mutation(graphene.ObjectType):
    create_domain = CreateDomain.Field()
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
