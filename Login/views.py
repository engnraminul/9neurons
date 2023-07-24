from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

#Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

#Message Module
from django.contrib import messages

from Login.models import User
from django.urls import reverse_lazy



def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        country = request.POST.get('country')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        github = request.POST.get('github')
        gender = request.POST.get('Gender')
        birth_date= request.POST.get('birth_date')
        university = request.POST.get('university')
        profile_picture = request.FILES.get('profile_picture')

        if User.objects.filter(email=email).exists():
            error_message = "This email is already registered. Please use a different email."
            return render(request, 'Login/registration.html', {'error_message': error_message})

        if not email or not password or not birth_date:
            error_message = "Email, Password, Birth Date fields are required for form fill-up."
            return render(request, 'Login/registration.html', {'error_message': error_message})


        user = User(email=email, password=password, full_name=full_name,
                          country=country,address=address, phone=phone, university=university,
                          gender=gender, birth_date=birth_date,  github=github, profile_picture=profile_picture)
        user.save()
        messages.success(request, "Your account create successfully")
        #return HttpResponseRedirect(reverse('Main:home'))

    return render(request, 'Login/registration.html')
    


from django.contrib.auth.views import LoginView




def profile(request):
    profile = User.objects.get(user=request.user)
    return render(request, 'Login/profile.html', {'profile': profile})


