from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('accounts/signup/', views.signup, name='signup'),
  path('accounts/<int:user_id>/profile/', views.create_profile, name='create profile'),
  path('profile/<int:user_id>/', views.profile, name='profile'),
]
