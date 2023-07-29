from django.urls import path
from Login import views


app_name = 'Login'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verify_email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),

]