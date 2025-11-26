from django.db import migrations


def seed_roles(apps, schema_editor):
    Rol = apps.get_model('App', 'Rol')
    roles = [
        ('Administrador general', 'Control total del sistema, usuarios y configuración'),
        ('Recepcionista', 'Gestiona turnos, agenda y registro de pacientes'),
        ('Veterinario clínico', 'Atiende consultas generales y revisa historia clínica'),
        ('Veterinario especialista', 'Atiende áreas específicas: cirugía, dermatología, cardiología'),
        ('Asistente veterinario', 'Ayuda en consultas y procedimientos'),
        ('Encargado de quirófano', 'Coordina cirugías, materiales y horarios del quirófano'),
        ('Técnico en laboratorio', 'Realiza análisis clínicos y carga resultados'),
        ('Encargado de farmacia', 'Gestiona medicamentos, stock y recetas'),
        ('Peluquero canino/felino', 'Recibe turnos estéticos'),
        ('Encargado de internación', 'Controla animales internados y medicación'),
        ('Cuidador temporal / guardería', 'Hospedaje y paseos'),
        ('Personal de limpieza', 'Mantenimiento y desinfección'),
        ('Encargado de stock / depósito', 'Control de insumos y productos'),
        ('Community manager / marketing', 'Gestión de redes y comunicación'),
        ('Cajero', 'Cobros y facturación en caja'),
        ('Contador', 'Balances, ingresos, gastos y reportes financieros'),
        ('Dueño / socio', 'Accede a reportes generales y administración avanzada'),
        ('Cliente registrado', 'Solicita turnos y revisa historial de su mascota'),
        ('Proveedor', 'Gestiona entregas y facturas de insumos'),
        ('Soporte técnico del sistema', 'Mantenimiento y actualización de plataforma'),
    ]
    for nombre, descripcion in roles:
        Rol.objects.get_or_create(nombre_rol=nombre, defaults={'descripcion': descripcion})


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_usuario_user'),
    ]

    operations = [
        migrations.RunPython(seed_roles),
    ]