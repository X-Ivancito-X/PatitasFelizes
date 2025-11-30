from django.urls import path, include
from .views import *
from .api import router as api_router
from rest_framework.routers import DefaultRouter

# El router crea automáticamente las URLs para /usuarios/
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', Index, name='Index'),
    path('contacto/', contacto, name='contacto'),
    path('turnos/', turnos, name='turnos'),
    path('nosotros/', nosotros, name='nosotros'),
    path('login/', ingresar, name='login'),
    path('logout/', salir, name='logout'),
    path('registro/', registro, name='registro'),
    path('auth/confirm-email/<str:token>/', confirmar_email, name='confirmar_email'),
    path('perfil/', perfil, name='perfil'),
    path('mascotas/', mascotas_list, name='mascotas_list'),
    path('mascotas/nueva/', mascota_create, name='mascota_create'),
    path('panel/turnos/', turnos_admin_list, name='turnos_admin_list'),
    path('panel/turnos/nuevo/', turno_create, name='turno_create'),
    path('panel/turnos/editar/<int:pk>/', turno_edit, name='turno_edit'),
    path('panel/turnos/eliminar/<int:pk>/', turno_delete, name='turno_delete'),
    path('panel/veterinarios/', veterinarios_admin_list, name='veterinarios_admin_list'),
    path('panel/veterinarios/nuevo/', veterinario_create, name='veterinario_create'),
    path('panel/veterinarios/editar/<int:pk>/', veterinario_edit, name='veterinario_edit'),
    path('panel/veterinarios/eliminar/<int:pk>/', veterinario_delete, name='veterinario_delete'),
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
    # Acciones específicas por rol
    path('roles/acciones/quirofano/inventario/', accion_quirofano_inventario, name='accion_quirofano_inventario'),
    path('roles/acciones/quirofano/calendario/', accion_quirofano_calendario, name='accion_quirofano_calendario'),
    path('roles/acciones/laboratorio/resultados/', accion_laboratorio_resultados, name='accion_laboratorio_resultados'),
    path('roles/acciones/laboratorio/estudios/', accion_laboratorio_estudios, name='accion_laboratorio_estudios'),
    path('roles/acciones/farmacia/stock/', accion_farmacia_stock, name='accion_farmacia_stock'),
    path('roles/acciones/farmacia/entregas/', accion_farmacia_entregas, name='accion_farmacia_entregas'),
    path('roles/acciones/peluqueria/servicios/', accion_peluqueria_servicios, name='accion_peluqueria_servicios'),
    path('roles/acciones/internacion/medicacion/', accion_internacion_medicacion, name='accion_internacion_medicacion'),
    path('roles/acciones/guarderia/agenda/', accion_guarderia_agenda, name='accion_guarderia_agenda'),
    path('roles/acciones/guarderia/actividades/', accion_guarderia_actividades, name='accion_guarderia_actividades'),
    path('roles/acciones/limpieza/plan/', accion_limpieza_plan, name='accion_limpieza_plan'),
    path('roles/acciones/stock/inventario/', accion_stock_inventario, name='accion_stock_inventario'),
    path('roles/acciones/stock/alertas/', accion_stock_alertas, name='accion_stock_alertas'),
    path('roles/acciones/marketing/campanas/', accion_marketing_campanas, name='accion_marketing_campanas'),
    path('roles/acciones/marketing/metricas/', accion_marketing_metricas, name='accion_marketing_metricas'),
    path('roles/acciones/cajero/cobros/', accion_cajero_cobros, name='accion_cajero_cobros'),
    path('roles/acciones/cajero/comprobantes/', accion_cajero_comprobantes, name='accion_cajero_comprobantes'),
    path('roles/acciones/contador/reportes/', accion_contador_reportes, name='accion_contador_reportes'),
    path('roles/acciones/contador/resumen/', accion_contador_resumen, name='accion_contador_resumen'),
    path('roles/acciones/proveedor/entregas/', accion_proveedor_entregas, name='accion_proveedor_entregas'),
    path('roles/acciones/proveedor/facturas/', accion_proveedor_facturas, name='accion_proveedor_facturas'),
    path('roles/acciones/soporte/logs/', accion_soporte_logs, name='accion_soporte_logs'),
    # API Email para pruebas con Postman
    path('api/mail/send/', api_send_email, name='api_send_email'),
    path('api/auth/password/reset/', api_password_reset, name='api_password_reset'),
    path('api/', include(api_router.urls)),
    # Conexion con Postman
    path('api/', include(router.urls)),
    
]
