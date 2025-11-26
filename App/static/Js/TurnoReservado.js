document.addEventListener('DOMContentLoaded', function () {
  var fecha = document.getElementById('fecha');
  if (fecha) {
    var today = new Date().toISOString().split('T')[0];
    fecha.setAttribute('min', today);
  }
  var form = document.getElementById('turnosForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      var email = document.getElementById('email');
      var telefono = document.getElementById('telefono');
      var hora = document.getElementById('hora');
      var nombreDueno = document.getElementById('nombreDueno');
      var nombreMascota = document.getElementById('nombreMascota');
      var ok = true;
      if (email && !/^\S+@\S+\.\S+$/.test(email.value)) { ok=false; alert('Email inválido'); }
      if (telefono && !/^\+?\d{7,15}$/.test(telefono.value)) { ok=false; alert('Teléfono inválido'); }
      if (hora && !/^\d{2}:\d{2}$/.test(hora.value)) { ok=false; alert('Hora inválida'); }
      if (nombreDueno && nombreDueno.value.trim().length<2) { ok=false; alert('Nombre del dueño es requerido'); }
      if (nombreMascota && nombreMascota.value.trim().length<2) { ok=false; alert('Nombre de la mascota es requerido'); }
      if(!ok){ e.preventDefault(); return; }
    });
  }
});