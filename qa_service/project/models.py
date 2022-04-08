from django.contrib.auth.models import User
from django.db import models


class U(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
