from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='profile/', default='profile/base_photo.jpg')
    biography = models.CharField(max_length=1000, null=True)
    profile_url = models.IntegerField(default=0)
    # questions = models.ManyToManyField(class, 'Вопросы')
    # answers = models.ManyToManyField(class, 'Ответы')
    # likes = models.ManyToManyField(class, 'Лайки')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
