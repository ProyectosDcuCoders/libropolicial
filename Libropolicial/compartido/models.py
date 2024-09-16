from django.db import models

# Create your models here.

class CuartoGuardiaUSH(models.Model):
    cuarto = models.CharField(max_length=1)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.cuarto

    def delete(self, *args, **kwargs):
        self.activo = False
        self.save()

