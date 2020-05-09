from django.db import models

# Create your models here.


"""
Estos modelos siguen el estandar creado por ISPmail 
si hay algo raro es que los nombres estan de acuerdo a ese estandar
Los nombres de las tablas están en plural por el estandar de ISPmail 
"""


class Domain(models.Model):
    """Dominos virtuales"""
    name = models.URLField(max_length=50, unique=True)

    class Meta:
        db_table = 'virtual_domains'

    def __str__(self):
        return self.name


class User(models.Model):
    """Usuarios del correo electronico"""
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    quota = models.BigIntegerField()

    class Meta:
        db_table = 'virtual_users'

    def __str__(self):
        return self.email


class Alias(models.Model):
    """Alias y redirecciones"""
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    source = models.CharField(max_length=250)
    destination = models.CharField(max_length=250)

    class Meta:
        db_table = 'virtual_aliases'
