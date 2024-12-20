
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from . models import urls
import randomcharactergenerator
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm

# Create your views here.

def home(request):
    return render(request , 'home.html')

#Login/ Logout/ Register

# Register user view
def registeruser(request):
    if request.user.is_authenticated:  # Check if user is already logged in
        return redirect('home')  # Redirect to home page if the user is authenticated

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the new user with first_name and last_name
            user = form.save()

            # Store success message and redirect to login page
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f'Account created successfully for {first_name} {last_name}! You can now log in.')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')  # Error message
    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {'form': form})

# Login user view
def userlogin(request):
    if request.user.is_authenticated:  # Check if user is already logged in
        return redirect('home')  # Redirect to home page if the user is authenticated

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')  # Redirect to a home page after successful login
            else:
                messages.error(request, 'Invalid username or password. Please try again.')  # Invalid credentials
        else:
            messages.error(request, 'Please fill in both username and password.')  # Form validation error
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

# Logout user view
def logoutuser(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # Redirect to login page after logout



@login_required(login_url="login")
def dashboard(request):
    links = urls.objects.filter(created_by = request.user)
    total_visits = urls.objects.filter(created_by = request.user).aggregate(Sum('visits'))

    if request.method == 'POST':
        name = request.POST['name']
        link = request.POST['link']
        unique_code = randomcharactergenerator.rand_code(4)
        if not urls.objects.filter(unique_code= unique_code).exists():
            short_url = str(request.scheme) + '://' + str(request.META["HTTP_HOST"]) + "/r/" + str(unique_code)
            urls.objects.create(name=name , link= link , unique_code=unique_code , short_url=short_url , created_by = request.user)
            messages.success(request , 'Link is succesfully created')
            return redirect('dashboard')
    # print(total_visits["visits__sum"])
    context={
        'links':links,
        'total_visits':total_visits
        
        }
        
    return render(request , 'dashboard.html', context)


@login_required(login_url="login")
def redirect_link(request , unique_code):
    link = urls.objects.get(unique_code=unique_code)

    link.visits+=1
    link.save()
    return redirect(link.link)



@login_required(login_url="login")
def delete_link(request,unique_code):
    urls.objects.filter(unique_code=unique_code).delete()
    messages.success(request, ('Your Link was successfully Deleted!'))
    return redirect('dashboard')



@login_required(login_url="login")
def analytics(request , unique_code ):
    links = urls.objects.get(unique_code=unique_code)
    context = {
        'links':links
    }

    return render(request , 'analytics.html' , context)


# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)
