from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    age = models.DateField(format("Birth Date:"), auto_now=False, auto_now_add=False)
    image = models.ImageField(null=True, blank=True, upload_to = '')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(null=True)

    def __str__(self):
        return self.name

class TravelPost(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    body = models.TextField()
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True, upload_to = '')

    def __str__(self):
        return self.title

class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=CASCADE)
    travelpost = models.ForeignKey(TravelPost, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)
