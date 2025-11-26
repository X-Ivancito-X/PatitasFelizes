from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def requires_roles(*role_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            usuario = getattr(request.user, 'usuario_profile', None)
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if not usuario or not usuario.rol or usuario.rol.nombre_rol not in role_names:
                messages.error(request, 'No tienes permisos para acceder a esta sección')
                return redirect('Index')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator