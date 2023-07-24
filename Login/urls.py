from django.urls import path
from Login import views


app_name = 'Login'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),

]