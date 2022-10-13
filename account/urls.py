from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit-account/', views.edit, name='edit'),
    path('add-car/', views.add_car, name='add_car'),
    path('search/', views.car_search, name='car_search'),

    # login / logout urls
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),


    #Change password urls
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='account/templates/registration/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/templates/registration/password_change_done.html'),
         name='password_change_done'),
    ]