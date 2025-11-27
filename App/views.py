from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import *
from .models import *
from .utils.permissions import requires_roles

def Index(request):
    return render(request, 'Index.html')

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        mensaje = request.POST.get('mensaje')
    # Aquí procesar el formulario (guardar en BD, enviar email, etc.)
        messages.success(request, '¡Gracias por contactarnos!')
        return redirect('contacto')

    return render(request, 'Page/Contacto.html')

def turnos(request):
    if request.method == 'POST':
        # Procesar datos del turno
        nombreDueno = request.POST.get('nombreDueno')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        # ... resto de campos
        # Guardar en base de datos
        messages.success(request, '¡Turno reservado exitosamente!')
        return redirect('turnos')
    
    return render(request, 'Page/Turnos.html')

def nosotros(request):
    return render(request, 'Page/Nosotros.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            username = form.cleaned_data.get('usuario') or email
            telefono = form.cleaned_data.get('telefono')
            direccion = form.cleaned_data.get('direccion')
            password = form.cleaned_data['password']
            user = Usuario.objects.filter(email=email).first()
            if user:
                messages.error(request, 'El email ya está registrado en el sistema')
            else:
                auth_user = User.objects.create_user(username=username, email=email, password=password, first_name=nombre, last_name=apellido)
                rol_cliente, _ = Rol.objects.get_or_create(nombre_rol='Cliente')
                usuario = Usuario.objects.create(nombre=nombre, apellido=apellido, email=email, contrasena='(hash-autenticación-django)', telefono=telefono, direccion=direccion, rol=rol_cliente, user=auth_user)
                login(request, auth_user)
                messages.success(request, 'Registro exitoso')
                return redirect('Index')
    else:
        form = RegistroForm()
    return render(request, 'Page/Auth/registro.html', {'form': form})

def ingresar(request):
    if request.method == 'POST':
        identifier = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=identifier, password=password)
        if not user and '@' in (identifier or ''):
            try:
                found = User.objects.get(email=identifier)
                user = authenticate(request, username=found.username, password=password)
            except User.DoesNotExist:
                user = None
        if user:
            login(request, user)
            return redirect('Index')
        messages.error(request, 'Credenciales inválidas')
    return render(request, 'Page/Auth/login.html')

def salir(request):
    logout(request)
    return redirect('Index')

@login_required
def perfil(request):
    usuario = getattr(request.user, 'usuario_profile', None)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        if usuario:
            usuario.telefono = telefono
            usuario.save()
        messages.success(request, 'Perfil actualizado')
        return redirect('Index')
    return redirect('Index')

@login_required
@requires_roles('Administrador general', 'Recepcionista', 'Veterinario clínico', 'Veterinario especialista')
def mascotas_list(request):
    q = request.GET.get('q', '').strip()
    especie = request.GET.get('especie', '').strip()
    order = request.GET.get('order', 'nombre')
    mascotas_qs = Mascota.objects.all()
    if q:
        mascotas_qs = mascotas_qs.filter(models.Q(nombre__icontains=q) | models.Q(raza__icontains=q))
    if especie:
        mascotas_qs = mascotas_qs.filter(especie__iexact=especie)
    if order:
        mascotas_qs = mascotas_qs.order_by(order)
    paginator = Paginator(mascotas_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    especies = list(Mascota.objects.values_list('especie', flat=True).distinct())
    usuario = getattr(request.user, 'usuario_profile', None)
    rol_nombre = usuario.rol.nombre_rol if usuario and usuario.rol else ''
    return render(request, 'Page/Mascotas/list.html', {
        'page_obj': page_obj,
        'q': q,
        'order': order,
        'especie': especie,
        'especies': especies,
        'rol_nombre': rol_nombre,
    })

@login_required
@requires_roles('Administrador general', 'Recepcionista', 'Veterinario clínico')
def mascota_create(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            # Asociar al dueño autenticado si tiene perfil Usuario
            usuario = getattr(request.user, 'usuario_profile', None)
            if usuario:
                mascota.duenio = usuario
            else:
                messages.error(request, 'Tu usuario no tiene perfil de Usuario asignado')
                return redirect('mascotas_list')
            mascota.save()
            messages.success(request, 'Mascota creada')
            return redirect('mascotas_list')
    else:
        form = MascotaForm()
    return render(request, 'Page/Mascotas/form.html', {'form': form})
@login_required
@requires_roles('Administrador general', 'Recepcionista')
def turnos_admin_list(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')
    order = request.GET.get('order', 'fecha')
    turnos_qs = Turno.objects.select_related('mascota', 'veterinario')
    if q:
        turnos_qs = turnos_qs.filter(mascota__nombre__icontains=q)
    if estado:
        turnos_qs = turnos_qs.filter(estado=estado)
    if order:
        turnos_qs = turnos_qs.order_by(order)
    paginator = Paginator(turnos_qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    usuario = getattr(request.user, 'usuario_profile', None)
    rol_nombre = usuario.rol.nombre_rol if usuario and usuario.rol else ''
    return render(request, 'Page/TurnosAdmin/List.html', {'page_obj': page_obj, 'q': q, 'estado': estado, 'order': order, 'rol_nombre': rol_nombre})

@login_required
@requires_roles('Administrador general', 'Recepcionista')
def turno_create(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turno creado')
            return redirect('turnos_admin_list')
    else:
        form = TurnoForm()
    return render(request, 'Page/TurnosAdmin/Form.html', {'form': form})

@login_required
@requires_roles('Administrador general', 'Recepcionista')
def turno_edit(request, pk):
    turno = Turno.objects.get(pk=pk)
    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turno actualizado')
            return redirect('turnos_admin_list')
    else:
        form = TurnoForm(instance=turno)
    return render(request, 'Page/TurnosAdmin/Form.html', {'form': form})

@login_required
@requires_roles('Administrador general', 'Recepcionista')
def turno_delete(request, pk):
    turno = Turno.objects.get(pk=pk)
    turno.delete()
    messages.success(request, 'Turno eliminado')
    return redirect('turnos_admin_list')

@login_required
def administracion(request):
    # Métricas simples
    total_turnos = Turno.objects.count()
    cancelados = Turno.objects.filter(estado='CANCELADO').count()
    reservados = Turno.objects.filter(estado='RESERVADO').count()
    disponibles = Turno.objects.filter(estado='DISPONIBLE').count()
    proximos = Turno.objects.order_by('fecha', 'hora')[:5]
    from django.utils import timezone
    from datetime import timedelta
    hoy = timezone.localdate()
    por_vencer = Turno.objects.filter(estado='RESERVADO', fecha__gte=hoy, fecha__lte=hoy + timedelta(days=2)).count()
    try:
        internaciones_curso = Internacion.objects.filter(estado='EN_CURSO', fecha_alta__isnull=True).count()
    except Exception:
        internaciones_curso = 0
    usuario = getattr(request.user, 'usuario_profile', None)
    rol_nombre = usuario.rol.nombre_rol if usuario and usuario.rol else ''
    return render(request, 'Page/Administracion.html', {
        'total_turnos': total_turnos,
        'cancelados': cancelados,
        'reservados': reservados,
        'disponibles': disponibles,
        'proximos': proximos,
        'por_vencer': por_vencer,
        'internaciones_curso': internaciones_curso,
        'rol_nombre': rol_nombre,
    })
