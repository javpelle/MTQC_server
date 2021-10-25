from django.db import models

# Create your models here.


class User(models.Model):
    email = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=64, null=False)
    token = models.CharField(max_length=100, null=True)
    emailVerified = models.BooleanField(default=False)
