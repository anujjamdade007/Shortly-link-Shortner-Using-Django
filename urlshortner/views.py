
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from . models import urls
import randomcharactergenerator
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request , 'home.html')

#Login/ Logout/ Register


def userlogin(request):
    page= 'login'
    form = UserForm()
    #hide the login page for alredy logged users
    if request.user.is_authenticated:
        return redirect('dashboard')
    

    if request.method == 'POST':
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request , 'username not found')

        user = authenticate(request , username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request ,"User Successfully Logged In")

            return redirect('home')
        else:
            messages.error(request ,"Username or Password not found")
        
    
    context={'page':page,
             'form':form,}
        
    return render(request ,'login.html' , context)

def logoutuser(request):
    logout(request)
    messages.success(request , 'User Is succesfully logged out')
    return redirect('login')

def registeruser(request):
    page= 'register'
    form = UserRegistrationForm()

    #hide the register page for alredy logged users
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST )
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request , 'user is succesfully created')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request , 'something went wrong')


    context={
        'page':page,
        'form':form,
        }
    return render(request , 'signup.html' , context )




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
    print(total_visits["visits__sum"])
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
