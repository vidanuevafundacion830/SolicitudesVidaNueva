from django.contrib import admin
from django.urls import path, include
from solicitudes import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('solicitudes.urls')),
]


handler404 = views.error_404
handler500 = views.error_500
handler403 = views.error_403
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATICFILES_DIRS[0]
)