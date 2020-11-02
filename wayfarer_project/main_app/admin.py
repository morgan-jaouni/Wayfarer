from django.contrib import admin
from .models import City, Profile, TravelPost

# Register your models here.
admin.site.register(Profile)
admin.site.register(TravelPost)
admin.site.register(City)