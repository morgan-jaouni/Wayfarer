from django.http import request
from main_app.models import City, Profile, TravelPost
from main_app.forms import PostForm, ProfileForm
from django.shortcuts import render, redirect
from django.template import RequestContext

# --------------------------------------- AUTH IMPORTS
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# --------------------------------------- INDEX
def index(request):
    return render(request, 'index.html')

# --------------------------------------- AUTH VIEWS
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create profile', user_id=user.id)
    else:
        error_message = 'Invalid Sign Up - Try Again'
        form = UserCreationForm()
        context = {'form': form, 'error_message': error_message}
        return render(request, 'registration/signup.html', context)

# --------------------------------------- PROFILE
def create_profile(request, user_id):
    error_message = ''
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user_id = user_id
            new_form.save()

        return redirect('profile', user_id=user_id)
    else:
        error_message = 'Invalid Sign Up - Try Again'
        form = ProfileForm()
        context = {'form': form, 'error_message': error_message}
        return render(request, 'registration/profiles.html', context)

@login_required
def profile(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    travelposts = TravelPost.objects.filter(author_id=profile.id)
    context = {
        'profile': profile, 
        'user_id': user_id,
        'travelposts' : travelposts
        }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request, user_id):
    profile = Profile.objects.get(user_id=user_id)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance = profile)
        if profile_form.is_valid():
            updated_profile=profile_form.save()
            return redirect('profile', updated_profile.user_id)

    else:
        form= ProfileForm(instance= profile)
        context = {'form':form, 'profile':profile}
        return render(request, 'profile/edit.html', context)

def profile_home(request):
    current_user = request.user
    return redirect('profile', user_id=current_user.id)

# --------------------------------------- POSTS
def travelpost_show(request, travelpost_id):
    travelpost = TravelPost.objects.get(id=travelpost_id)
    context = {
        'travelpost': travelpost,
        'travelpost_id': travelpost_id
    }
    return render(request, 'travelposts/show.html', context)

@login_required
def travelpost_edit(request, travelpost_id):
    error_message = ''
    travelpost = TravelPost.objects.get(id=travelpost_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=travelpost)
        if form.is_valid():
            edit_form = form.save()
            return redirect('travelpost_show', travelpost_id)


    else:
        error_message = 'Invalid Post - Try Again'
        form = PostForm(instance=travelpost)
        context = {'form': form, 'error_message': error_message, 'travelpost_id': travelpost_id}
        return render(request, 'travelposts/edit.html', context)

@login_required
def travelpost_new(request, city_id):
    error_message = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        current_user = request.user
        profile = Profile.objects.get(user_id=current_user.id)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.author_id = profile.id
            new_form.city_id = city_id
            new_form.save()

        return redirect('show_city', city_id)

    else:
        error_message = 'Invalid Post - Try Again'
        form = PostForm()
        context = {'form': form, 'error_message': error_message, 'city_id': city_id}
        return render(request, 'travelposts/new.html', context)


@login_required
def travelpost_delete(request, travelpost_id):
    TravelPost.objects.get(id=travelpost_id).delete()
    return redirect('profile_home')
# --------------------------------------- ERROR HANDLING
# def handler404(request, exception):
#     return render(request, '404.html', status=404)
# def handler500(request):
#     return render(request, '500.html', status=500)

# --------------------------------------- CITIES

def show_city(request, city_id):
    city = City.objects.get(id=city_id)
    travelposts = TravelPost.objects.filter(city_id=city_id)
    context = {
        'city': city,
        'travelposts': travelposts,
    }
    return render(request, 'city/show.html', context)


