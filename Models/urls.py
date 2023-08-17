from django.urls import path
from . import views

app_name = 'Models'

urlpatterns = [
    path('create-model/', views.create_model, name='create_model'),
    path('models',views.models_list, name='models_list'),
]