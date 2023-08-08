from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Model, Files
from Models.Forms import ModelFilesForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# @login_required
# def create_model(request):
#     if request.user.user_type in ['Member', 'Premium Member']:
#         if request.method == 'POST':
#             form = ModelForm(request.POST)
#             if form.is_valid():
#                 model = form.save(commit=False)
#                 model.author = request.user
#                 model.save()
#                 return HttpResponseRedirect(reverse('Login:profile'))
#         else:
#             form = ModelForm()
#         return render(request, 'model/create_model.html', {'form': form})
#     else:
#         return render(request, 'loging/profile.html.html')


@login_required
def create_model(request):
    if request.user.user_type in ['Member', 'Premium Member']:
        if request.method == 'POST':
            form = ModelFilesForm(request.POST, request.FILES)
            if form.is_valid():
                model = form.save(commit=False)
                model.author = request.user
                model.save()
                
                # Save the associated files
                uploaded_files = request.FILES.getlist('file')  # Get list of uploaded files
                
                for uploaded_file in uploaded_files:
                    Files.objects.create(model_name=model, file=uploaded_file)
                
                return HttpResponseRedirect(reverse('Login:profile'))
        else:
            form = ModelFilesForm()
        return render(request, 'model/create_model.html', {'form': form})
    else:
        return render(request, 'permission_denied.html')

