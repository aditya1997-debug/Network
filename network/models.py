from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name="followed_by", blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=72)
    post = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now())
    liked_by = models.ManyToManyField(User, related_name='liked_by', blank=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f"{self.user}'s post {self.id}"

    def likes(self):
        return self.liked_by.count()

    
    

