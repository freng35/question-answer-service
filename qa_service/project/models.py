from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='profile/', default='profile/base_photo.jpg')
    biography = models.CharField(max_length=1000, null=True)
    profile_url = models.IntegerField(default=0)


class Question(models.Model):
    user_created = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    theme = models.CharField(max_length=200, null=False)
    text = models.CharField(max_length=3000, null=False)


class Answer(models.Model):
    user_answered = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000)


class Like(models.Model):
    user_from_like = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE)
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
