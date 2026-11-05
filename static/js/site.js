// Superblexy Media — site behaviour (no dependencies)
(function () {
  // Keep the footer year current without a rebuild
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Gentle reveal-on-scroll
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('js-reveal');
    var els = document.querySelectorAll('.vgrid .item, .ruled-item, .ruled-photo, .card, .step, .tm, .shorts .item, .gallery img, .about-story > *');
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el, i) { el.classList.add('reveal'); el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el); });
  }

  // Mobile menu
  var header = document.querySelector('.site-header');
  var btn = document.querySelector('.menu-btn');
  if (btn) btn.addEventListener('click', function () {
    var open = header.classList.toggle('menu-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // YouTube click-to-play (loads the player only when clicked)
  document.querySelectorAll('.yt[data-id]').forEach(function (el) {
    var img = el.querySelector('img');
    // YouTube returns a 120px placeholder when maxres doesn't exist: fall back to hqdefault
    var fix = function () { if (img.naturalWidth <= 120 && img.src.indexOf('maxresdefault') > -1) img.src = img.src.replace('maxresdefault', 'hqdefault'); };
    if (img) { if (img.complete && img.naturalWidth) fix(); img.addEventListener('load', fix); img.addEventListener('error', fix); }
    el.addEventListener('click', function () {
      var id = el.getAttribute('data-id');
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1';
      f.title = el.getAttribute('aria-label') || 'YouTube video';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.allowFullscreen = true;
      el.innerHTML = '';
      el.appendChild(f);
      el.style.cursor = 'default';
    }, { once: true });
  });

  // Testimonial carousel arrows
  document.querySelectorAll('[data-carousel]').forEach(function (wrap) {
    var track = wrap.querySelector('.tm-track');
    var prev = wrap.querySelector('[data-prev]');
    var next = wrap.querySelector('[data-next]');
    function step() { var c = track.children[0]; return c ? c.getBoundingClientRect().width + 40 : 300; }
    function update() {
      prev.disabled = track.scrollLeft < 8;
      next.disabled = track.scrollLeft + track.clientWidth > track.scrollWidth - 8;
    }
    prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });

  // Calendly: load the widget only when it scrolls near view
  var cal = document.querySelector('.calendly-inline-widget');
  if (cal) {
    var loaded = false;
    var load = function () {
      if (loaded) return; loaded = true;
      var s = document.createElement('script');
      s.src = 'https://assets.calendly.com/assets/external/widget.js';
      s.async = true;
      document.body.appendChild(s);
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e, o) { if (e[0].isIntersecting) { load(); o.disconnect(); } }, { rootMargin: '400px' }).observe(cal);
    } else load();
  }

  // "Send another message" resets the success panel
  var again = document.querySelector('[data-fs-again]');
  if (again) again.addEventListener('click', function () {
    var f = document.querySelector('#contact-form'), ok = document.getElementById('form-success');
    ok.hidden = true; f.hidden = false;
    var h1 = f.parentNode.querySelector('h1'); if (h1) h1.hidden = false;
    f.querySelector('[name=name]').focus();
  });

  // Contact form (Web3Forms)
  var form = document.querySelector('#contact-form');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var status = form.querySelector('.form-status');
    var submit = form.querySelector('button[type=submit]');
    if (form.querySelector('[name=botcheck]').checked) return;
    status.className = 'form-status';
    status.textContent = 'Sending…';
    var nm = (form.querySelector('[name=name]').value || '').trim();
    form.querySelector('[name=subject]').value = 'New enquiry from ' + (nm || 'the website') + ' · superblexymedia.com';
    submit.disabled = true;
    fetch(form.action, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j.success, j: j }; }); })
      .then(function (res) {
        if (res.ok) {
          var ok = document.getElementById('form-success');
          var first = nm.split(' ')[0];
          ok.querySelector('[data-fs-name]').textContent = first ? ', ' + first : '';
          ok.querySelector('[data-fs-email]').textContent = form.querySelector('[name=email]').value || 'your email';
          form.reset();
          status.className = 'form-status';
          status.textContent = '';
          form.hidden = true;
          var h1 = form.parentNode.querySelector('h1'); if (h1) h1.hidden = true;
          ok.hidden = false;
          ok.scrollIntoView({ behavior: 'smooth', block: 'center' });
          ok.focus({ preventScroll: true });
        } else throw new Error((res.j && res.j.message) || 'failed');
      })
      .catch(function () {
        status.className = 'form-status err';
        status.innerHTML = 'Something went wrong sending your message. Please email us at <a href="mailto:info@superblexymedia.com">info@superblexymedia.com</a>.';
      })
      .finally(function () { submit.disabled = false; });
  });
})();
