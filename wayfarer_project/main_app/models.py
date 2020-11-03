from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(("Email:"), max_length=254)
    city = models.CharField(max_length=100)
    age = models.DateField(format("Birth Date:"), auto_now=False, auto_now_add=False)
    join_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    image = models.URLField()

    def __str__(self):
        return self.title

