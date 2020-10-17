from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.


class Company(models.Model):
    """Datos de la empresa que nos contrata el servicio"""
    name = models.CharField(max_length=50)
    id_number = models.CharField(  # RUC o DNI
        max_length=11, unique=True,
        validators=(
            RegexValidator(
                regex=r'^[0-9]$',
                message="Enter a valid ID number it must be only numbers"
            ),)
    )
    domain = models.ManyToManyField("virtual.Domain")

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

    def get_domains(self):  # este es para el admin
        return '\n'.join([domain.name for domain in self.domain.all()])


class DomainAdmin(models.Model):
    """Datos del administador de dominio,
    tendrá un enlace directo al usuario de nuestro sistema"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    company = models.ManyToManyField('Company')

    def __str__(self):
        return self.user.username
