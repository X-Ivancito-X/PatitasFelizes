document.addEventListener('DOMContentLoaded', function () {
  var carousel = document.getElementById('heroCarousel');
  if (!carousel) return;

  var slidesData = [
    {
      image: '/happy-dog-at-veterinary-clinic.jpg',
      title: 'Cuidado Profesional para tu Mascota',
      description: 'Más de 15 años brindando servicios veterinarios de calidad',
    },
    {
      image: '/cat-being-examined-by-veterinarian.jpg',
      title: 'Atención Personalizada',
      description: 'Cada mascota es única y merece un trato especial',
    },
    {
      image: '/veterinary-clinic-waiting-room.jpg',
      title: 'Instalaciones Modernas',
      description: 'Equipamiento de última generación para el mejor diagnóstico',
    },
  ];

  function getBgClass(image) {
    switch (image) {
      case '/happy-dog-at-veterinary-clinic.jpg':
        return 'bg-happy-dog';
      case '/cat-being-examined-by-veterinarian.jpg':
        return 'bg-cat-exam';
      case '/veterinary-clinic-waiting-room.jpg':
        return 'bg-waiting-room';
      default:
        return '';
    }
  }

  function buildCarousel() {
    carousel.innerHTML = '';

    slidesData.forEach(function (item, idx) {
      var slide = document.createElement('div');
      slide.className = 'carousel-slide' + (idx === 0 ? ' active' : '');

      var bg = document.createElement('div');
      var bgClass = getBgClass(item.image);
      bg.className = 'carousel-slide-bg' + (bgClass ? ' ' + bgClass : '');

      var overlay = document.createElement('div');
      overlay.className = 'carousel-overlay';
      bg.appendChild(overlay);
      slide.appendChild(bg);

      var content = document.createElement('div');
      content.className = 'carousel-content';
      var inner = document.createElement('div');
      var h1 = document.createElement('h1');
      h1.textContent = item.title;
      var p = document.createElement('p');
      p.textContent = item.description;
      var a = document.createElement('a');
      a.href = '/turnos';
      a.className = 'btn btn-lg';
      a.textContent = 'Reservar Turno Ahora';
      inner.appendChild(h1);
      inner.appendChild(p);
      inner.appendChild(a);
      content.appendChild(inner);
      slide.appendChild(content);
      carousel.appendChild(slide);
    });

    var controls = document.createElement('div');
    controls.className = 'carousel-controls';
    var prevBtn = document.createElement('button');
    prevBtn.className = 'carousel-btn';
    prevBtn.id = 'prevBtn';
    prevBtn.setAttribute('aria-label', 'Previous slide');
    prevBtn.textContent = '❮';
    var nextBtn = document.createElement('button');
    nextBtn.className = 'carousel-btn';
    nextBtn.id = 'nextBtn';
    nextBtn.setAttribute('aria-label', 'Next slide');
    nextBtn.textContent = '❯';
    controls.appendChild(prevBtn);
    controls.appendChild(nextBtn);
    carousel.appendChild(controls);

    var indicatorsWrap = document.createElement('div');
    indicatorsWrap.className = 'carousel-indicators';
    slidesData.forEach(function (_, idx) {
      var b = document.createElement('button');
      b.className = 'carousel-indicator' + (idx === 0 ? ' active' : '');
      b.setAttribute('data-slide', String(idx));
      indicatorsWrap.appendChild(b);
    });
    carousel.appendChild(indicatorsWrap);
  }

  buildCarousel();

  var slides = carousel.querySelectorAll('.carousel-slide');
  var indicators = carousel.querySelectorAll('.carousel-indicator');
  var prevBtn = document.getElementById('prevBtn');
  var nextBtn = document.getElementById('nextBtn');
  var currentSlide = 0;
  var autoPlayInterval;

  function showSlide(index) {
    slides.forEach(function (s) { s.classList.remove('active'); });
    indicators.forEach(function (i) { i.classList.remove('active'); });
    slides[index].classList.add('active');
    if (indicators[index]) indicators[index].classList.add('active');
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }

  function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
  }

  function startAutoPlay() {
    stopAutoPlay();
    autoPlayInterval = setInterval(nextSlide, 5000);
  }

  function stopAutoPlay() {
    if (autoPlayInterval) clearInterval(autoPlayInterval);
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', function () {
      nextSlide();
      startAutoPlay();
    });
  }
  if (prevBtn) {
    prevBtn.addEventListener('click', function () {
      prevSlide();
      startAutoPlay();
    });
  }

  indicators.forEach(function (indicator, index) {
    indicator.addEventListener('click', function () {
      currentSlide = index;
      showSlide(currentSlide);
      startAutoPlay();
    });
  });

  showSlide(currentSlide);
  startAutoPlay();
});