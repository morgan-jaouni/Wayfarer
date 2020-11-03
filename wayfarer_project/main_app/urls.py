from django.contrib import admin
from django.urls import path, include
from . import views
# error handling issues
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
  # ------------------------------------- STATIC
  path('', views.index, name='index'),
  path('accounts/signup/', views.signup, name='signup'),

  # ------------------------------------- USERS ROUTES
  path('accounts/<int:user_id>/profile/', views.create_profile, name='create profile'),
  path('profile/<int:user_id>/', views.profile, name='profile'),

  # ------------------------------------- PROFILE ROUTES
  path('profile/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),
  path('accounts/profile/', views.profile_home, name='profile_home'),

    # ------------------------------------- POST ROUTES
  path('travelpost/<int:travelpost_id>/', views.show_travelpost, name='show'),
] 

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# handler404 = views.handler404
# handler500 = views.handler500