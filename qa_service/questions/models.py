from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    user_created = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    theme = models.CharField(max_length=200, null=False)
    text = models.CharField(max_length=3000, null=False)

    def likes(self):
        return Like.objects.filter(question=self)

    def amount_of_likes(self):
        return len(self.likes())

    def answers(self):
        return Answer.objects.filter(question=self)

    def amount_of_answers(self):
        return len(self.answers())


class Answer(models.Model):
    user_answered = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000)


class Like(models.Model):
    user_from_like = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
