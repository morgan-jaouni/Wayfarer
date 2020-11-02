from main_app.models import Profile, TravelPost
from main_app.forms import ProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

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

def show_travelpost(request, travelpost_id):
    travelpost = TravelPost.objects.get(id=travelpost_id)
    context = {
        'travelpost': travelpost,
        'travelpost_id': travelpost_id
    }
    return render(request, 'travelposts/show.html', context)

