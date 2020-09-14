from django.db import models
from .lib import password
from django.core.validators import RegexValidator

# Create your models here.


"""
Estos modelos siguen el estandar creado por ISPmail 
si hay algo raro es que los nombres estan de acuerdo a ese estandar
Los nombres de las tablas están en plural por el estandar de ISPmail 
"""


class Domain(models.Model):
    """Dominos virtuales"""
    name = models.TextField(
        max_length=50,
        unique=True,
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


class User(models.Model):
    """Usuarios del correo electronico"""
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True, null=False, default=None)
    quota = models.PositiveBigIntegerField(default=1)

    __previous_password = None

    class Meta:
        db_table = 'virtual_users'

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__previous_password = self.password

    def __str__(self):
        return self.email


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
        super(User, self).save(*args, **kwargs)

    def quota_used(self):
        """Obtener la cuota del usuario via IMAP"""
        pass


class Alias(models.Model):
    """Alias y redirecciones"""
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    source = models.CharField(max_length=250)
    destination = models.CharField(max_length=250)

    class Meta:
        db_table = 'virtual_aliases'
