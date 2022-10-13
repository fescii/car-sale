from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm,UserRegistrationForm,\
    UserEditForm, ProfileEditForm, CarForm, ImageForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from carinfo.models import Car, Image


# Create your views here.
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

def user_login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        #form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                     return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def register(request):
    user_form = UserRegistrationForm(request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
        else:
            user_form = UserRegistrationForm()
            return render(request,
                          'account/register.html',
                          {'user_form': user_form})
    return render(request,
                          'account/register.html',
                          {'user_form': user_form})

@login_required
def edit(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)

            return render(request,
                          'account/edit.html',
                          {'user_form': user_form,
                           'profile_form': profile_form})
    return render(request,
                          'account/edit.html',
                          {'user_form': user_form,
                           'profile_form': profile_form})

@login_required
def add_car(request):
    car_form = CarForm(request.POST)
    if request.method == 'POST':
        if car_form.is_valid():
            new_car = car_form.save(commit=False)
            new_car.seller = request.user
            new_car.save()
        else:
            car_form = CarForm(request.POST)
            return render(request,
                          'car/add-car.html',
                          {'car_form': car_form,
                           'section': 'add'})
    return render(request,
                          'car/add-car.html',
                          {'car_form': car_form,
                           'section': 'add'})


