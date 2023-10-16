from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    user_id = models.AutoField(primary_key=True)

    def save(self, *args, **kwargs):
        # Obtén el último ID en la tabla
        last_id = Usuario.objects.aggregate(max_id=models.Max('user_id'))['max_id'] or 0

        # Aumenta el ID en 100 y asigna el nuevo valor
        self.user_id = last_id + 100

        super().save(*args, **kwargs)