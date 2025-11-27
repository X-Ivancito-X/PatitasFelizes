from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Modelo Roles
class Rol(models.Model):
    """Representa los diferentes roles de usuarios en el sistema (Administrador, Veterinario, Cliente, etc.)."""
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Rol")
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción del Rol")

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['nombre_rol']

    def __str__(self):
        return self.nombre_rol

# Modelo Usuarios
class Usuario(models.Model):
    """Representa a los usuarios del sistema (Clientes, Veterinarios, Administradores)."""
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True, verbose_name="Correo Electrónico")
    # Nota: En Django, la autenticación y el hashing de contraseñas se manejan a menudo con el modelo User de Django,
    # pero para replicar tu tabla, se usa CharField, asumiendo que el hashing se hace antes de guardar.
    contrasena = models.CharField(max_length=255, validators=[MinLengthValidator(8)], verbose_name="Contraseña (Hash)")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono de Contacto")
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Dirección")
    # Relación con Roles (id_rol INT FK)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, verbose_name="Rol del Usuario")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_profile', null=True, blank=True, verbose_name="Usuario de Autenticación")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol.nombre_rol})"

# Modelo Mascotas
class Mascota(models.Model):
    """Representa a las mascotas registradas en la veterinaria, propiedad de un usuario cliente."""
    id_mascota = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre de la Mascota")
    especie = models.CharField(max_length=50, verbose_name="Especie (Ej: Perro, Gato)")
    raza = models.CharField(max_length=50, blank=True, null=True, verbose_name="Raza (Opcional)")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    # Relación con Usuarios (id_duenio INT FK) - Asume que el FK apunta a un usuario con rol "Cliente"
    duenio = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mascotas', verbose_name="Dueño")

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.especie})"

    def edad(self):
        from datetime import date
        if not self.fecha_nacimiento:
            return None
        hoy = date.today()
        years = hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
        return years

# Modelo Veterinaria (información adicional para usuarios con rol Veterinario)
class Veterinario(models.Model):
    """Información adicional para los usuarios que tienen el rol de 'Veterinario'."""
    id_veterinario = models.AutoField(primary_key=True)
    # Relación con Usuarios (id_usuario INT FK) - Se asume que el usuario debe tener el rol "Veterinario"
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_veterinario', verbose_name="Usuario Asociado")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad (Ej: Cirugía, Clínica General)")

    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"

    def __str__(self):
        return f"Dr(a). {self.usuario.apellido} ({self.especialidad})"

# Opciones para el campo 'estado' en Turnos
ESTADO_CHOICES = [
    ('DISPONIBLE', 'Disponible'),
    ('RESERVADO', 'Reservado'),
    ('CANCELADO', 'Cancelado'),
    ('ATENDIDO', 'Atendido'),
]

# Modelo Turnos
class Turno(models.Model):
    """Representa un turno programado para la atención de una mascota."""
    id_turno = models.AutoField(primary_key=True)
    # Relación con Mascota (id_mascota INT FK)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='turnos', verbose_name="Mascota")
    # Relación con Veterinario (id_veterinario INT FK)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT, related_name='turnos_asignados', verbose_name="Veterinario Asignado")
    fecha = models.DateField(verbose_name="Fecha del Turno")
    hora = models.TimeField(verbose_name="Hora del Turno")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE', verbose_name="Estado del Turno")

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        unique_together = ('fecha', 'hora', 'veterinario') # Para evitar doble reserva a la misma hora con el mismo veterinario
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"Turno de {self.mascota.nombre} con Dr(a). {self.veterinario.usuario.apellido} el {self.fecha}"

# Modelo Historial Clinico
class HistorialClinico(models.Model):
    """Almacena los registros de atención médica para una mascota."""
    id_historial = models.AutoField(primary_key=True)
    # Relación con Mascota (id_mascota INT FK)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historiales', verbose_name="Mascota")
    # Relación con Veterinario (id_veterinario INT FK)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT, related_name='registros_creados', verbose_name="Veterinario Atendió")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora de Atención") # Se puede usar auto_now_add para registrar cuándo se creó
    diagnostico = models.TextField(verbose_name="Diagnóstico")
    tratamiento = models.TextField(verbose_name="Tratamiento / Indicaciones")

    class Meta:
        verbose_name = "Historial Clínico"
        verbose_name_plural = "Historiales Clínicos"
        ordering = ['-fecha'] # Ordenar del más reciente al más antiguo

    def __str__(self):
        return f"Registro #{self.id_historial} de {self.mascota.nombre} ({self.fecha.strftime('%Y-%m-%d')})"

# Modelo Internación
ESTADO_INTERNACION_CHOICES = [
    ('EN_CURSO', 'En curso'),
    ('ALTA', 'Alta médica'),
]

class Internacion(models.Model):
    id_internacion = models.AutoField(primary_key=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='internaciones', verbose_name="Mascota")
    fecha_ingreso = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    fecha_alta = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Alta")
    estado = models.CharField(max_length=20, choices=ESTADO_INTERNACION_CHOICES, default='EN_CURSO', verbose_name="Estado")

    class Meta:
        verbose_name = "Internación"
        verbose_name_plural = "Internaciones"
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return f"Internación #{self.id_internacion} de {self.mascota.nombre} ({self.get_estado_display()})"
