from django.contrib import admin
from django.urls import path, include

#show media files
from django.conf import settings
from django.contrib. staticfiles.urls import static

from Main import views
app_name = 'Main'
urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
    path('account/', include('Login.urls')),
    path('models/', include('Models.urls')),
    path('ckeditor/', include("ckeditor_uploader.urls"))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)