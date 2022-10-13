from statistics import mode
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm,UserRegistrationForm,\
    UserEditForm, ProfileEditForm, CarForm,SearchForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from carinfo.models import Car
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


# Create your views here.
def dashboard(request):
    car_list = Car.objects.all()
    # Pagination with 3 posts per page
    paginator = Paginator(car_list, 5)
    page_number = request.GET.get('page', 1)
    cars = paginator.page(page_number)
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                  'cars': cars})


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
    profile_form = ProfileEditForm(instance=request.user.profile,files=request.FILES)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile,files=request.FILES)

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
    car_form = CarForm(request.POST,files=request.FILES)
    if request.method == 'POST':
        if car_form.is_valid():
            new_car = car_form.save(commit=False)
            new_car.seller = request.user
            new_car.save()
            return HttpResponseRedirect(reverse('dashboard'))
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


def car_search(request):
    search_form = SearchForm(request.GET)
    location = None
    query = None
    results = []
    if request.GET:
        model  = request.GET['model']
        location = request.GET['location']
        results = Car.objects.filter(model=model,location=location)
        query = True
        return render(request,'car/search.html',
                        {'search_form': search_form,
                       'query': query,
                       'results': results})
    return render(request,'car/search.html',
                      {'search_form': search_form,
                       'query': query,
                       'results': results})


