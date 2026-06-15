from django.contrib import admin
from django.urls import path, include
from solicitudes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('solicitudes.urls')),
]

# Estos handler están perfectos, déjalos así
handler404 = views.error_404
handler500 = views.error_500
handler403 = views.error_403

# ELIMINA todo el bloque de static(...) que tenías abajo.
# WhiteNoise ya lo gestiona automáticamente por ti.