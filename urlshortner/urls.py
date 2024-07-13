from django.contrib import admin
from django.urls import include, path
from. import views


urlpatterns = [
    path('' , views.home , name='home'),
    path('login/' , views.userlogin , name='login'),
    path('register/' , views.registeruser , name='register'),
    path('logout/' , views.logoutuser , name='logout'),
    path('dashboard/' , views.dashboard , name='dashboard'),
    path('r/<str:unique_code>' , views.redirect_link , name='redirect_link'),
    path('delete/<str:unique_code>' , views.delete_link , name='delete_link'),
    path('analytics/<str:unique_code>' , views.analytics , name='analytics'),

]
