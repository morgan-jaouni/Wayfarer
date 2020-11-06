from django.http import request
from django.template import context
from main_app.models import City, Like, Profile, TravelPost
from main_app.forms import CityPostForm, PostForm, ProfileForm, SignUpForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate

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
        form = SignUpForm(request.POST)
        sub_form = ProfileForm(request.POST)
        if form.is_valid() & sub_form.is_valid():
            user = form.save()
            new_form = sub_form.save(commit=False)
            new_form.user_id = user.id
            if request.FILES:
                new_form.image = request.FILES['image']
            new_form.save()
            login(request, user)
            return redirect('profile', user_id=user.id)
        else:
            error_message = form.non_field_errors
            sub_form = ProfileForm()
            context = {'form': form, 'sub_form': sub_form, 'error_message': error_message}
            return render(request, 'registration/signup.html', context)
    else:
        form = SignUpForm()
        sub_form = ProfileForm()
        context = {'form': form, 'sub_form': sub_form,}## 'error_message': error_message}
        return render(request, 'registration/signup.html', context)

# --------------------------------------- PROFILE
@login_required
def profile(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    travelposts = TravelPost.objects.filter(author_id=profile.id)
    
    context = {
        'profile': profile, 
        'user_id': user_id,
        'travelposts' : travelposts,
        }

    return render(request, 'profile.html', context)


@login_required
def edit_profile(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    user = request.user.id=user_id
    if user:
        if request.method == 'POST':
                form = ProfileForm(request.POST, instance = profile)
                if form.is_valid():
                    profile.image = request.FILES['image']
                    updated_profile=form.save()
                return redirect('profile', updated_profile.user_id)
        else:
            form = ProfileForm(instance = profile)
            context = {
                'form': form,
            }
            return render(request, 'profile/edit.html', context)
    else:
        return redirect('index')

def profile_home(request):
    current_user = request.user
    return redirect('profile', user_id=current_user.id)

# --------------------------------------- POSTS
def travelpost_show(request, travelpost_id):
    profile = Profile.objects.get(user_id = request.user.id)
    travelpost = TravelPost.objects.get(id=travelpost_id)
    posts = TravelPost.objects.filter(author_id = profile.id)
    liked = Like.objects.filter(profile_id=profile.id, travelpost_id=travelpost.id)
    travelpost.likes +=1
    context = {
        'travelpost': travelpost,
        'travelpost_id': travelpost_id,
        'liked': liked,
    }
    return render(request, 'travelposts/show.html', context)

def like(request, travelpost_id):
    profile = Profile.objects.get(user_id = request.user.id)
    post = TravelPost.objects.get(id=travelpost_id)
    new, created = Like.objects.get_or_create(profile_id=profile.id, travelpost_id=travelpost_id)
    if not created:
        if post.likes > 0:
            post.likes -= 1
            post.save()
        new.delete()
        return redirect('travelpost_show', travelpost_id)
    else:
        post.likes += 1
        post.save()
        return redirect('travelpost_show', travelpost_id)

@login_required
def travelpost_edit(request, travelpost_id):
    error_message = ''
    travelpost = TravelPost.objects.get(id=travelpost_id)
    user = request.user.id=travelpost.author.user_id
    if user:
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

    else:
        return redirect('index')

@login_required
def travelpost_new(request, city_id):
    error_message = ''
    if request.method == 'POST':
        if city_id > 0:
            form = CityPostForm(request.POST)
        else:
            form = PostForm(request.POST)
        current_user = request.user
        profile = Profile.objects.get(user_id=current_user.id)

        if form.is_valid():
            new_form = form.save(commit=False)
            if request.FILES:
                new_form.image = request.FILES['image']
            new_form.image = request.FILES['image']
            new_form.author_id = profile.id
            if city_id > 0:
                new_form.city_id = city_id
            new_form.save()
            return redirect('show_city', new_form.city_id)
    else:
        if city_id > 0:
            form = CityPostForm()
        else:
            form = PostForm()
        context = {'form': form, 'error_message': error_message, 'city_id': city_id}
        return render(request, 'travelposts/new.html', context)


@login_required
def travelpost_delete(request, travelpost_id):
    travelpost = TravelPost.objects.get(id=travelpost_id)
    user = request.user.id=travelpost.author.user_id
    if user:
        TravelPost.objects.get(id=travelpost_id).delete()
        return redirect('profile_home')
    else:
        return redirect('index')
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


