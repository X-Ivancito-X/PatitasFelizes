document.addEventListener('DOMContentLoaded', function () {
  var navToggle = document.getElementById('navToggle');
  var navMenu = document.getElementById('navMenu');
  if (!navToggle || !navMenu) return;
  navToggle.addEventListener('click', function () {
    navMenu.classList.toggle('active');
  });
});