document.addEventListener('DOMContentLoaded', function(){
  var open = document.getElementById('openPerfil');
  var modal = document.getElementById('perfilModal');
  var close = document.getElementById('closePerfil');
  if(open && modal){
    open.addEventListener('click', function(e){ e.preventDefault(); modal.style.display='block'; modal.setAttribute('aria-hidden','false'); });
  }
  if(close && modal){
    close.addEventListener('click', function(){ modal.style.display='none'; modal.setAttribute('aria-hidden','true'); });
  }
});