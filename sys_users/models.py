from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings

# Create your models here.


class Company(models.Model):
    """Datos de la empresa que nos contrata el servicio"""
    name = models.CharField(max_length=50)
    id_number = models.CharField(  # RUC o DNI
        max_length=11, unique=True,
        validators=(
            RegexValidator(
                regex=r'^[0-9]*$',
                message="Enter a valid ID number it must be only numbers"
            ),
        )
    )
    start_date = models.DateField(
        auto_now_add=True, null=True, blank=True)
    domain = models.ManyToManyField("virtual.Domain")
    quota_total = models.PositiveBigIntegerField(default=1073741824)

    class Meta:
        verbose_name_plural = 'Companies'

    def __init__(self, *args, **kwargs):
        super(Company, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.quota_total < settings.BYTE_TO_GIGABYTE_FACTOR:
            self.quota_total *= settings.BYTE_TO_GIGABYTE_FACTOR
        super(Company, self).save(*args, **kwargs)

    def get_domains(self):  # este es para el admin
        return '\n'.join([domain.name for domain in self.domain.all()])

    def quota_totalgb(self):
        return self.quota_total / settings.BYTE_TO_GIGABYTE_FACTOR

    def get_used_quota(self):
        """returns quota used by the domain

        Returns:
            int: quota used by the domain
        """
        self.all_quota = 0
        for domain in self.domain.all():
            self.all_quota += domain.get_quota()
        return self.all_quota

    def get_used_quotagb(self):
        """returns quota used by the domain

        Returns:
            int: quota used by the domain
        """
        self.all_quota = 0
        for domain in self.domain.all():
            self.all_quota += domain.get_quota()
        return self.all_quota / settings.BYTE_TO_GIGABYTE_FACTOR

    def get_percnet_used_quota(self):
        return (self.get_used_quota() / self.quota_total) * 100

    def is_full(self):
        """
        Returns:
            bool: true if there is no more space
        """
        return self.get_used_quota() >= self.quota_total


class DomainAdmin(models.Model):
    """Datos del administador de dominio,
    tendrá un enlace directo al usuario de nuestro sistema"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=False, null=False)
    company = models.ManyToManyField('Company')

    def __str__(self):
        return self.user.username
