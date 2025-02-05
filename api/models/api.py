from django.db import models

class Api(models.Model):
    api_id = models.CharField(max_length=50,unique=True)
    url = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    status = models.BooleanField(default=False)
    