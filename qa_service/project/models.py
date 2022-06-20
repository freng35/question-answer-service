from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='avatars/users', default='avatars/users/0.png')
    biography = models.CharField(max_length=1000, null=True)
    profile_url = models.IntegerField(default=0)
    # questions = models.ManyToManyField(class, 'Вопросы')
    # answers = models.ManyToManyField(class, 'Ответы')
    # likes = models.ManyToManyField(class, 'Лайки')

