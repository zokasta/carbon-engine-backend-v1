from django.db import models

class Api(models.Model):
    url = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    status = models.BooleanField(default=True)
    