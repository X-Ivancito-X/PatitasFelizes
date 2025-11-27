from django.urls import path, include
from .views import *
from .api import router as api_router

urlpatterns = [
    path('', Index, name='Index'),
    path('contacto/', contacto, name='contacto'),
    path('turnos/', turnos, name='turnos'),
    path('nosotros/', nosotros, name='nosotros'),
    path('login/', ingresar, name='login'),
    path('logout/', salir, name='logout'),
    path('registro/', registro, name='registro'),
    path('perfil/', perfil, name='perfil'),
    path('mascotas/', mascotas_list, name='mascotas_list'),
    path('mascotas/nueva/', mascota_create, name='mascota_create'),
    path('panel/turnos/', turnos_admin_list, name='turnos_admin_list'),
    path('panel/turnos/nuevo/', turno_create, name='turno_create'),
    path('panel/turnos/editar/<int:pk>/', turno_edit, name='turno_edit'),
    path('panel/turnos/eliminar/<int:pk>/', turno_delete, name='turno_delete'),
    path('administracion/', administracion, name='administracion'),
    # Sectores por rol
    path('roles/asistente/', rol_asistente_veterinario, name='rol_asistente_veterinario'),
    path('roles/quirofano/', rol_quirofano, name='rol_quirofano'),
    path('roles/laboratorio/', rol_laboratorio, name='rol_laboratorio'),
    path('roles/farmacia/', rol_farmacia, name='rol_farmacia'),
    path('roles/peluqueria/', rol_peluqueria, name='rol_peluqueria'),
    path('roles/internacion/', rol_internacion, name='rol_internacion'),
    path('roles/guarderia/', rol_guarderia, name='rol_guarderia'),
    path('roles/limpieza/', rol_limpieza, name='rol_limpieza'),
    path('roles/stock/', rol_stock, name='rol_stock'),
    path('roles/marketing/', rol_marketing, name='rol_marketing'),
    path('roles/cajero/', rol_cajero, name='rol_cajero'),
    path('roles/contador/', rol_contador, name='rol_contador'),
    path('roles/duenio/', rol_duenio, name='rol_duenio'),
    path('roles/cliente/', rol_cliente, name='rol_cliente'),
    path('roles/proveedor/', rol_proveedor, name='rol_proveedor'),
    path('roles/soporte/', rol_soporte, name='rol_soporte'),
    path('api/', include(api_router.urls)),

    
]
