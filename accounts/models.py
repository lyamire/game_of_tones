from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user)