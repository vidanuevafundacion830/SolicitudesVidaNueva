from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('guardar', views.guardar),
    path('guardar/', views.guardar, name='guardar'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-secretaria/', views.dashboard_secretaria, name='dashboard_secretaria'),
    path('solicitudes_asignadas/', views.solicitudes_asignadas, name='solicitudes_asignadas'),
    path('solicitud/<int:solicitud_id>/', views.solicitud_detalle, name='solicitud_detalle'),
    path('dashboard-docente/', views.dashboard_docente, name='dashboard_docente'),
    path('docente/solicitud/<int:solicitud_id>/', views.docente_detalle, name='docente_detalle'),
    path('dashboard-superadmin/', views.dashboard_superadmin, name='dashboard_superadmin'),
    path('registro_admin/', views.registro_admin, name='registro_admin'),
    path('editar_usuario/<int:admin_id>/', views.editar_usuario, name='editar_usuario'),
    path('actualizar_usuario/<int:admin_id>/', views.actualizar_usuario, name='actualizar_usuario'),
    path('eliminar_usuario/<int:admin_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('solicitud/eliminar/<int:solicitud_id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
]
