from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Business(models.Model):
    """Datos de la empresa que nos contrata el servicio"""
    name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=11)  # RUC o DNI

    def __str__(self):
        return self.name

class DomainAdmin(models.Model):
    """Datos del administador de dominio,
    tendrá un enlace directo al usuario de nuestro sistema"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    domain = models.ManyToManyField("virtual.Domain")
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
