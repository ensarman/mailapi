from django.db import models
from lib import password
from django.core.validators import RegexValidator
from lib.DoveAdmHTTPClient import DoveAdmHTTPClient
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.


"""
Estos modelos siguen el estandar creado por ISPmail
si hay algo raro es que los nombres estan de acuerdo a ese estandar
Los nombres de las tablas están en plural por el estandar de ISPmail
"""


class Domain(models.Model):
    """Dominos virtuales"""
    name = models.CharField(
        max_length=50, unique=True,
        validators=(
            RegexValidator(
                regex=r'^[a-zA-Z0-9-]*\.[a-z]*$',
                message="Enter a valid domain name"
            ),)
    )

    class Meta:
        db_table = 'virtual_domains'

    def __str__(self):
        return self.name

    def get_companies(self):  # este es para el admin
        return '\n'.join(company.name for company in self.company_set.all())


class User(models.Model):
    """Usuarios del correo electronico"""
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(
        max_length=100, blank=True, null=False, default=None)
    quota = models.PositiveBigIntegerField(default=1)

    __previous_password = None
    __byte_to_gigabyte_factor = 1073741824
    __dovehttp = None

    class Meta:
        db_table = 'virtual_users'

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__previous_password = self.password
        self.__dovehttp = DoveAdmHTTPClient(
            apiurl=settings.DOVECOT_HTTP['url'],
            user=settings.DOVECOT_HTTP['user'],
            password=settings.DOVECOT_HTTP['password'],
        )
        if self.id:
            """Only enters here only if the user exists"""
            storage_quota = self.__dovehttp.get_quota(user=self.email)
            self.quota_used = int(storage_quota['value'])
            self.quota_percent = int(storage_quota['percent'])

    def __str__(self):
        return self.email

    def quota_gb(self):
        return self.quota / self.__byte_to_gigabyte_factor

    def get_company(self):
        pass

    def save(self, *args, **kwargs):
        if not self.id:
            """si no hay ID es que es un nuevo usuario"""
            if self.password:
                """encripta el password"""
                self.password = password.crypt_pass(self.password)
            else:
                """
                Si es Usuario nuevo y no se ha definido password
                pwgen genera un password raw aleatorio y luego lo encipta
                """
                self.password = password.crypt_pass(password.pw_gen())
        else:
            """si es que hay id es que es un update"""
            if self.password != self.__previous_password:
                """significa que ha sido editado"""
                self.password = password.crypt_pass(self.password)

        self.quota *= self.__byte_to_gigabyte_factor
        super(User, self).save(*args, **kwargs)


class Alias(models.Model):
    """Alias y redirecciones"""
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    source = models.CharField(max_length=250)
    destination = models.CharField(max_length=250)

    class Meta:
        db_table = 'virtual_aliases'
