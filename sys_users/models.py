from django.db import models
from django.contrib.auth.models import User
from django.core.validators import DecimalValidator

# Create your models here.

class Company(models.Model):
    """Datos de la empresa que nos contrata el servicio"""
    name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=11)  # RUC o DNI
    domain = models.ManyToManyField("virtual.Domain")

    def __str__(self):
        return self.name


class DomainAdmin(models.Model):
    """Datos del administador de dominio,
    tendrá un enlace directo al usuario de nuestro sistema"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    company = models.ManyToManyField('Company')

    def __str__(self):
        return self.user.username
