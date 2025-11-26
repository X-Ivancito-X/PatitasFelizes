from rest_framework import viewsets, routers, serializers
from .models import *

class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = '__all__'

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = '__all__'

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer
    def get_queryset(self):
        qs = Mascota.objects.all()
        q = self.request.query_params.get('q', '').strip()
        if q:
            qs = qs.filter(nombre__icontains=q)
        return qs

class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    def get_queryset(self):
        qs = Turno.objects.all()
        estado = self.request.query_params.get('estado', '').strip()
        q = self.request.query_params.get('q', '').strip()
        if estado:
            qs = qs.filter(estado=estado)
        if q:
            qs = qs.filter(mascota__nombre__icontains=q)
        return qs

router = routers.DefaultRouter()
router.register(r'mascotas', MascotaViewSet)
router.register(r'turnos', TurnoViewSet)