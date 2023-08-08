from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

#Authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
#Message Module
from django.contrib import messages
from Login.models import User

#Email Veryfication
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils.html import format_html

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist

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


        user = User(email=email, full_name=full_name,
                          country=country,address=address, phone=phone, university=university,
                          gender=gender, birth_date=birth_date,  github=github, profile_picture=profile_picture)
        user.set_password(password)
        
        # Set the user as inactive until they verify their email
        user.is_active = True

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
        user.email_verify = True
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
        user = authenticate(request, email=email, password=password)

        if user is not None:
            print("User is not None")  # For debugging

            # Check if the user is authenticated before logging them in
            if user.email_verify == True:
                login(request, user)
                messages.success(request, "You are logged in successfully")
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, "Your account is inactive. Please check your email.")
        else:
            print("User is None")  # For debugging
            messages.error(request, "Incorrect email or password. Please try again.")

    return render(request, 'Login/login.html')

    


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # Generate a unique token for password reset
            token = get_random_string(length=64)
            user.verification_token = token
            user.save()

            # Send the password reset email
            current_site = get_current_site(request)
            subject = 'Password Reset Request'
            message = render_to_string('login/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })

            email = EmailMessage(subject, message, to=[user.email])
            email.send()

        messages.success(request, "If your email exists in our system, you will receive a password reset link shortly.")
        return redirect('Login:login')

    return render(request, 'login/forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and user.verification_token == token:
        # Valid token, proceed with password reset
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 == password2:
                user.set_password(password1)
                user.verification_token = None  # Clear the token after password reset
                user.save()

                update_session_auth_hash(request, user)  # Update the session with the new password
                messages.success(request, "Your password has been reset successfully. You can now log in with your new password.")
                return redirect('Login:login')
            else:
                messages.error(request, "Passwords do not match. Please try again.")
                return redirect('Login:reset_password', uidb64=uidb64, token=token)

        return render(request, 'login/reset_password.html')
    else:
        messages.error(request, "The password reset link is invalid or has expired. Please request a new one.")
        return redirect('Login:forgot_password')



@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, "You are logout successfully!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    profile = request.user
    return render(request, 'Login/profile.html', {'profile': profile})


