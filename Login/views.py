from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

#Authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
#Message Module
from django.contrib import messages
from Login.models import User
from django.urls import reverse_lazy

#Email Veryfication
import secrets
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string
from django.utils.html import format_html

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
        
        # Set the user as inactive until they verify their email
        user.is_active = False

        # Save the token and expiration time in the user's model
        token = get_random_string(length=64)
        print("Token:", token)

        # Save the token in the user's model
        user.verification_token = token
        user.save()
        

        # Send the verification email
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string('login/email_verification.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        
        email = EmailMessage(subject, message, to=[user.email])
        email.send()
        #messages.success(request, "Your account create successfully. We are verification link in your email" )
        success_message = format_html("Your account has been created successfully. We have sent a verification link to your email: <strong>{}</strong>", user.email)
        messages.success(request, success_message)
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'Login/registration.html')



def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print("Received Token:", token)  # Add this line to check the token received in the URL

    if user is not None and user.verification_token == token:
        # Mark the user as active
        user.is_active = True
        user.verification_token = None  # Clear the token after verification
        user.save()
        messages.success(request, "Your email has been verified successfully. You can now log in.")
        return HttpResponseRedirect(reverse('home'))
    else:
        messages.error(request, "The verification link is invalid. Please request a new one.")
        return HttpResponseRedirect(reverse('home'))

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use the 'authenticate' function from 'django.contrib.auth'
        #user = authenticate(request, email=email, password=password)
        try:
            user = User.objects.get(email=email, password=password)
            auth_login(request, user)
            messages.success(request, "You are logged in successfully")
            return HttpResponseRedirect(reverse('home'))
        except User.DoesNotExist:
            messages.error(request, "Incorrect email or password. Please try again.")


        # if user is not None:
        #     auth_login(request, user)
        #     messages.success(request, "You are logged in successfully")
        #     return HttpResponseRedirect(reverse('home'))
        # else:
        #     messages.error(request, "Incorrect email or password. Please try again.")

    return render(request, 'Login/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, "You are logout successfully!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    profile = request.user
    return render(request, 'Login/profile.html', {'profile': profile})


