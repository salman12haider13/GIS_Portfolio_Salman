(() => {
  'use strict';
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.primary-nav');
  document.documentElement.classList.add('js');
  if (menu && nav) {
    menu.hidden = false;
    const closeMenu = () => {
      menu.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('click', event => { if (!event.target.closest('.site-nav')) closeMenu(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        closeMenu(); menu.focus();
      }
    });
    matchMedia('(min-width: 721px)').addEventListener('change', closeMenu);
  }

  const filters = document.querySelector('.filters');
  if (filters) {
    filters.hidden = false;
    const cards = [...document.querySelectorAll('.work-card')];
    const buttons = [...filters.querySelectorAll('button')];
    const applyFilter = (category, updateUrl = false) => {
      if (!buttons.some(button => button.dataset.filter === category)) category = 'all';
      let visible = 0;
      for (const card of cards) {
        card.hidden = category !== 'all' && card.dataset.category !== category;
        if (!card.hidden) visible++;
      }
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
      document.querySelector('.result-count').textContent = `${visible} ${visible === 1 ? 'project' : 'projects'}`;
      if (updateUrl) {
        const url = new URL(location.href);
        if (category === 'all') url.searchParams.delete('category');
        else url.searchParams.set('category', category);
        history.pushState(null, '', url);
      }
    };
    buttons.forEach(button => button.addEventListener('click', () => applyFilter(button.dataset.filter, true)));
    const fromUrl = () => applyFilter(new URL(location.href).searchParams.get('category') || 'all');
    addEventListener('popstate', fromUrl);
    fromUrl();
  }

  // Preserve links to the former single-page portfolio.
  if (/\/(?:index\.html)?$/.test(location.pathname)) {
    const legacy = {
      '#home': 'index.html', '#maps': 'work.html', '#projects': 'work.html?category=tools',
      '#profile': 'about.html', '#beyond': 'about.html#outside-work', '#experience': 'about.html#experience',
      '#case-study-geo-copilot': 'projects/geo-copilot.html',
      '#project-geo-copilot': 'projects/geo-copilot.html',
      '#project-logistics-routing': 'projects/logistics-routing.html',
      '#project-drone-route-automation': 'projects/drone-route-reporting.html',
      '#project-forestry-sampling': 'projects/forestry-sampling.html',
      '#project-ndvi-zonal-stats': 'projects/ndvi-zonal-stats.html',
      '#project-spatial-reference-checker': 'projects/spatial-reference-checker.html',
      '#project-csv-survey-points': 'projects/csv-survey-points.html',
      '#project-lidar-metadata': 'projects/lidar-metadata.html'
    };
    const followLegacy = () => { if (legacy[location.hash]) location.replace(legacy[location.hash]); };
    followLegacy();
    addEventListener('hashchange', followLegacy);
  }

  const dialog = document.querySelector('.map-dialog');
  if (dialog && typeof dialog.showModal === 'function') {
    const stage = dialog.querySelector('.map-stage');
    const img = stage.querySelector('img');
    const status = stage.querySelector('.viewer-status');
    const zoomIn = dialog.querySelector('[data-zoom="in"]');
    const zoomOut = dialog.querySelector('[data-zoom="out"]');
    const pointers = new Map();
    let scale = 1, base = 1, x = 0, y = 0, ready = false, trigger = null, serial = 0;
    let lastGesture = null;
    const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
    function render() {
      if (!ready) return;
      const width = img.naturalWidth * base * scale;
      const height = img.naturalHeight * base * scale;
      x = width <= stage.clientWidth ? (stage.clientWidth - width) / 2 : clamp(x, stage.clientWidth - width, 0);
      y = height <= stage.clientHeight ? (stage.clientHeight - height) / 2 : clamp(y, stage.clientHeight - height, 0);
      img.style.width = `${img.naturalWidth}px`;
      img.style.height = `${img.naturalHeight}px`;
      img.style.transform = `translate(${x}px, ${y}px) scale(${base * scale})`;
      zoomIn.disabled = scale >= Math.max(8, 1 / base);
      zoomOut.disabled = scale <= 1;
      stage.classList.toggle('is-draggable', scale > 1);
    }
    function fit() {
      if (!ready) return;
      base = Math.min(stage.clientWidth / img.naturalWidth, stage.clientHeight / img.naturalHeight);
      scale = 1; x = 0; y = 0; render();
    }
    function zoom(next, cx = stage.clientWidth / 2, cy = stage.clientHeight / 2) {
      if (!ready) return;
      next = clamp(next, 1, Math.max(8, 1 / base));
      const ratio = next / scale;
      x = cx - (cx - x) * ratio;
      y = cy - (cy - y) * ratio;
      scale = next; render();
    }
    document.querySelectorAll('[data-inspect]').forEach(link => {
      link.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        trigger = link; ready = false; img.hidden = true; pointers.clear(); lastGesture = null;
        status.hidden = false; status.textContent = 'Loading image…';
        dialog.querySelector('#viewer-title').textContent = link.dataset.title;
        dialog.querySelector('[data-original]').href = link.href;
        img.alt = link.closest('figure')?.querySelector('img')?.alt || link.dataset.title;
        zoomIn.disabled = true; zoomOut.disabled = true;
        document.body.style.overflow = 'hidden';
        dialog.showModal();
        const request = ++serial;
        img.onload = () => {
          if (request !== serial || !dialog.open) return;
          ready = true; fit(); img.hidden = false; status.hidden = true;
        };
        img.onerror = () => {
          if (request !== serial) return;
          status.textContent = 'This image could not be loaded. Try opening the original image.';
        };
        img.src = link.href;
      });
    });
    dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
    dialog.addEventListener('close', () => {
      serial++; ready = false; pointers.clear(); lastGesture = null;
      stage.classList.remove('is-dragging');
      document.body.style.overflow = '';
      trigger?.focus();
    });
    zoomIn.addEventListener('click', () => zoom(scale * 1.5));
    zoomOut.addEventListener('click', () => zoom(scale / 1.5));
    dialog.querySelector('[data-zoom="fit"]').addEventListener('click', fit);
    stage.addEventListener('wheel', event => {
      if (!ready) return;
      event.preventDefault();
      const rect = stage.getBoundingClientRect();
      zoom(scale * Math.exp(-event.deltaY * 0.002), event.clientX - rect.left, event.clientY - rect.top);
    }, { passive: false });
    stage.addEventListener('keydown', event => {
      if (['+', '=', '-', '0', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) event.preventDefault();
      if (event.key === '+' || event.key === '=') zoom(scale * 1.5);
      else if (event.key === '-') zoom(scale / 1.5);
      else if (event.key === '0') fit();
      else {
        if (event.key === 'ArrowLeft') x += 60;
        if (event.key === 'ArrowRight') x -= 60;
        if (event.key === 'ArrowUp') y += 60;
        if (event.key === 'ArrowDown') y -= 60;
        render();
      }
    });
    function gesture() {
      const points = [...pointers.values()];
      const a = points[0], b = points[1];
      if (!a) return null;
      return b ? { x: (a.x+b.x)/2, y: (a.y+b.y)/2, distance: Math.hypot(b.x-a.x, b.y-a.y) } : { ...a, distance: 0 };
    }
    stage.addEventListener('pointerdown', event => {
      if (!ready || (event.pointerType === 'mouse' && event.button !== 0)) return;
      stage.focus({ preventScroll: true });
      stage.setPointerCapture(event.pointerId);
      pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
      lastGesture = gesture();
      stage.classList.add('is-dragging');
    });
    stage.addEventListener('pointermove', event => {
      if (!pointers.has(event.pointerId)) return;
      pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
      const current = gesture();
      if (lastGesture && current) {
        if (current.distance && lastGesture.distance) {
          const rect = stage.getBoundingClientRect();
          zoom(scale * current.distance / lastGesture.distance, lastGesture.x-rect.left, lastGesture.y-rect.top);
        }
        x += current.x-lastGesture.x; y += current.y-lastGesture.y; render();
      }
      lastGesture = current;
    });
    const release = event => {
      pointers.delete(event.pointerId); lastGesture = gesture();
      if (!pointers.size) stage.classList.remove('is-dragging');
    };
    stage.addEventListener('pointerup', release);
    stage.addEventListener('pointercancel', release);
    stage.addEventListener('lostpointercapture', release);
    new ResizeObserver(() => { if (dialog.open && ready) fit(); }).observe(stage);
  }

  // Keep local preview visits out of the existing production analytics.
  if (['salmanhaider.pro', 'www.salmanhaider.pro'].includes(location.hostname)) {
    const analytics = document.createElement('script');
    analytics.async = true;
    analytics.src = 'https://www.googletagmanager.com/gtag/js?id=G-M8922B3N0S';
    document.head.append(analytics);
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', 'G-M8922B3N0S');
  }
})();
