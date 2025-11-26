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
    path('api/', include(api_router.urls)),

    
]