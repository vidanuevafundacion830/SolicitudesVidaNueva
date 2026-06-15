from django.contrib import admin
from django.urls import path, include, re_path # <--- Añade re_path aquí
from django.conf import settings
from django.views.static import serve # <--- Añade serve aquí

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('solicitudes.urls')),
]

urlpatterns += [
    re_path(r'^media/(?s)(.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]