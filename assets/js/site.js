/* =========================================================
   The Vijayran Palace — Sujan Motion & Interaction Engine
   Lenis Smooth Scroll + GSAP ScrollTrigger + Sujan Motion DNA
   ========================================================= */

(() => {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Lenis Smooth Scroll ---------- */
  let lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      wheelMultiplier: 0.95
    });

    if (window.gsap && window.ScrollTrigger) {
      gsap.registerPlugin(ScrollTrigger);
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((time) => lenis.raf(time * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = (time) => {
        lenis.raf(time);
        requestAnimationFrame(raf);
      };
      requestAnimationFrame(raf);
    }
  }

  /* Internal anchor scroll */
  $$('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const href = a.getAttribute('href');
      if (!href || href === '#' || href.length < 2) return;
      const target = $(href);
      if (!target) return;
      e.preventDefault();
      if (lenis) {
        lenis.scrollTo(target, { offset: -90 });
      } else {
        target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
      }
    });
  });

  /* ---------- Header Scroll Behavior ---------- */
  const header = $('.g_nav_w');
  const hero = $('.hero_s');

  const onScroll = () => {
    const y = window.scrollY || window.pageYOffset;
    if (header) {
      header.classList.toggle('scrolled', y > 30);
      header.classList.toggle('has-bg', !hero || y > 350);
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Fullscreen Menu Overlay ---------- */
  const menuTrigger = $('.menu_trigger');
  const menuOverlay = $('.g_nav_open');

  const toggleMenu = (open) => {
    if (!menuOverlay) return;
    const isOpen = open !== undefined ? open : !menuOverlay.classList.contains('open');
    menuOverlay.classList.toggle('open', isOpen);
    header?.classList.toggle('menu-open', isOpen);
    document.body.classList.toggle('no-scroll', isOpen);
    if (lenis) isOpen ? lenis.stop() : lenis.start();
  };

  menuTrigger?.addEventListener('click', () => toggleMenu());
  $$('a', menuOverlay || document.body).forEach((a) => {
    a.addEventListener('click', () => toggleMenu(false));
  });

  /* ---------- Book Now Dropdown ---------- */
  const bookWrapper = $('.book_wrapper');
  const bookBtn = $('.book_btn');

  bookBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    bookWrapper?.classList.toggle('open');
  });

  document.addEventListener('click', (e) => {
    if (bookWrapper && !bookWrapper.contains(e.target)) {
      bookWrapper.classList.remove('open');
    }
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      toggleMenu(false);
      bookWrapper?.classList.remove('open');
    }
  });

  /* ---------- Hero Ambient Video & Sound Toggle ---------- */
  const heroVideo = $('.hero_video');
  const soundBtn = $('.sound_trigger');

  if (heroVideo && soundBtn) {
    soundBtn.addEventListener('click', () => {
      heroVideo.muted = !heroVideo.muted;
      soundBtn.classList.toggle('is-on', !heroVideo.muted);
      if (!heroVideo.muted) {
        heroVideo.play().catch(() => {});
      }
    });
  }

  /* ---------- Sujan Motion: Line Reveals & Parallax ---------- */
  if (window.gsap && !reduce) {
    // Hero video smooth scale on scroll
    const mainVideo = $('.main_video');
    if (mainVideo && hero) {
      gsap.to(mainVideo, {
        scale: 1.25,
        ease: 'none',
        scrollTrigger: {
          trigger: hero,
          start: 'top top',
          end: 'bottom top',
          scrub: true
        }
      });

      // Hero text fade and lift
      gsap.to('.h_p, .scroll_cue, .sound_trigger', {
        opacity: 0,
        y: -30,
        ease: 'none',
        scrollTrigger: {
          trigger: hero,
          start: 'top top',
          end: '60% top',
          scrub: true
        }
      });
    }

    // Sujan line-masked reveal (.d_y > *)
    $$('.d_y > *').forEach((el) => {
      gsap.fromTo(
        el,
        { yPercent: 105, opacity: 0.2 },
        {
          yPercent: 0,
          opacity: 1,
          duration: 1.1,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: el.parentElement,
            start: 'top 90%',
            once: true
          }
        }
      );
    });

    // Certification quote banner parallax zoom
    const certImg = $('.c_img');
    const certSection = $('.certification_s');
    if (certImg && certSection) {
      gsap.fromTo(
        certImg,
        { yPercent: -8, scale: 1.0 },
        {
          yPercent: 8,
          scale: 1.15,
          ease: 'none',
          scrollTrigger: {
            trigger: certSection,
            start: 'top bottom',
            end: 'bottom top',
            scrub: true
          }
        }
      );
    }

    // Sticky story section parallax images
    const mm = gsap.matchMedia();
    mm.add('(min-width: 961px)', () => {
      $$('.story_items').forEach((item, idx) => {
        const speed = parseFloat(item.dataset.speed || 1.0);
        gsap.fromTo(
          item,
          { y: 80 * speed },
          {
            y: -100 * speed,
            ease: 'none',
            scrollTrigger: {
              trigger: item,
              start: 'top bottom',
              end: 'bottom top',
              scrub: 0.5
            }
          }
        );

        const img = item.querySelector('img');
        if (img) {
          gsap.fromTo(
            img,
            { scale: 1.02 },
            {
              scale: 1.12,
              ease: 'none',
              scrollTrigger: {
                trigger: item,
                start: 'top bottom',
                end: 'bottom top',
                scrub: true
              }
            }
          );
        }
      });
    });
  } else {
    // Fallback reveal via IntersectionObserver
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.style.transform = 'none';
          en.target.style.opacity = '1';
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.1 });

    $$('.d_y > *').forEach((el) => {
      el.style.transform = 'translateY(40px)';
      el.style.opacity = '0';
      el.style.transition = 'transform 0.9s cubic-bezier(0.2,0.7,0.2,1), opacity 0.9s';
      io.observe(el);
    });
  }

  /* ---------- Draggable Card Track (Stays) ---------- */
  $$('.camp_track').forEach((track) => {
    let isDown = false;
    let startX = 0;
    let scrollLeft = 0;
    let moved = 0;

    track.addEventListener('pointerdown', (e) => {
      if (e.pointerType !== 'mouse') return;
      isDown = true;
      moved = 0;
      startX = e.clientX;
      scrollLeft = track.scrollLeft;
      track.style.cursor = 'grabbing';
      track.style.scrollSnapType = 'none';
    });

    window.addEventListener('pointermove', (e) => {
      if (!isDown) return;
      const dx = e.clientX - startX;
      moved = Math.max(moved, Math.abs(dx));
      track.scrollLeft = scrollLeft - dx;
    });

    window.addEventListener('pointerup', () => {
      if (!isDown) return;
      isDown = false;
      track.style.cursor = 'grab';
      track.style.scrollSnapType = 'x proximity';
    });

    track.addEventListener('click', (e) => {
      if (moved > 6) {
        e.preventDefault();
        e.stopPropagation();
      }
    }, true);
  });

  /* ---------- Live Weather (Open-Meteo API for Kukas, Jaipur) ---------- */
  const LAT = 27.0167;
  const LON = 75.8833;

  const getWeatherIcon = (code, isDay = 1) => {
    if (code === 0 || code === 1) {
      return isDay
        ? '<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="12" fill="#D1A555"/><g stroke="#D1A555" stroke-width="2.5" stroke-linecap="round"><path d="M32 8v6M32 50v6M8 32h6M50 32h6M15 15l4 4M45 45l4 4M49 15l-4 4M19 45l-4 4"/></g></svg>'
        : '<svg viewBox="0 0 64 64"><path fill="#D1A555" d="M42 42A18 18 0 0 1 24 12a18 18 0 1 0 28 30 18 18 0 0 1-10 0z"/></svg>';
    }
    if (code === 2 || code === 3) {
      return '<svg viewBox="0 0 64 64"><circle cx="22" cy="24" r="9" fill="#D1A555"/><path fill="#E9E1D6" d="M22 50h26a9.5 9.5 0 0 0 1-18.9A13.5 13.5 0 0 0 23.6 32 8.4 8.4 0 0 0 22 50z"/></svg>';
    }
    if (code >= 51 && code <= 67) {
      return '<svg viewBox="0 0 64 64"><path fill="#E9E1D6" d="M19 38h28a9.5 9.5 0 0 0 1-18.9A14 14 0 0 0 20 21 8.5 8.5 0 0 0 19 38z"/><g stroke="#7FB2E6" stroke-width="2.2" stroke-linecap="round"><path d="M23 44l-3 8M33 44l-3 8M43 44l-3 8"/></g></svg>';
    }
    return '<svg viewBox="0 0 64 64"><path fill="#E9E1D6" d="M19 46h28a10.5 10.5 0 0 0 1.2-20.9A15 15 0 0 0 19.6 28 9.2 9.2 0 0 0 19 46z"/></svg>';
  };

  const getWeatherDesc = (code) => {
    if (code === 0) return 'Clear Sky';
    if (code === 1) return 'Mainly Clear';
    if (code === 2) return 'Partly Cloudy';
    if (code === 3) return 'Overcast';
    if (code >= 45 && code <= 48) return 'Morning Mist';
    if (code >= 51 && code <= 67) return 'Light Rain';
    if (code >= 80 && code <= 82) return 'Showers';
    if (code >= 95) return 'Thunderstorm';
    return 'Clear Sky';
  };

  const loadWeather = async () => {
    try {
      const res = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,is_day&daily=weather_code,temperature_2m_max,temperature_2m_min,sunset&timezone=Asia%2FKolkata&forecast_days=5`
      );
      const data = await res.json();
      if (!data || !data.current) return;

      const c = data.current;
      const d = data.daily;
      const temp = Math.round(c.temperature_2m);
      const desc = getWeatherDesc(c.weather_code);
      const icon = getWeatherIcon(c.weather_code, c.is_day);

      // Top bar chip
      const chip = $('[data-wx-chip]');
      if (chip) chip.innerHTML = `<span>Jaipur · ${temp}°C ${desc}</span>`;

      // Weather Card
      const card = $('.wx_card');
      if (card) {
        const iconEl = card.querySelector('.wx_icon');
        const tempEl = card.querySelector('.wx_temp_num');
        const descEl = card.querySelector('.wx_condition');
        const feelsEl = card.querySelector('[data-wx-feels]');
        const humEl = card.querySelector('[data-wx-hum]');
        const windEl = card.querySelector('[data-wx-wind]');
        const sunEl = card.querySelector('[data-wx-sun]');
        const daysEl = card.querySelector('.wx_forecast');

        if (iconEl) iconEl.innerHTML = icon;
        if (tempEl) tempEl.textContent = temp;
        if (descEl) descEl.textContent = desc;
        if (feelsEl) feelsEl.textContent = `${Math.round(c.apparent_temperature)}°C`;
        if (humEl) humEl.textContent = `${Math.round(c.relative_humidity_2m)}%`;
        if (windEl) windEl.textContent = `${Math.round(c.wind_speed_10m)} km/h`;
        if (sunEl && d.sunset && d.sunset[0]) {
          const sunsetTime = new Date(d.sunset[0]).toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit', hour12: true });
          sunEl.textContent = sunsetTime;
        }

        if (daysEl && d.time) {
          daysEl.innerHTML = d.time.slice(0, 5).map((t, idx) => {
            const dayName = idx === 0 ? 'Today' : new Date(t + 'T00:00').toLocaleDateString('en-IN', { weekday: 'short' });
            const dayIcon = getWeatherIcon(d.weather_code[idx], 1);
            const max = Math.round(d.temperature_2m_max[idx]);
            const min = Math.round(d.temperature_2m_min[idx]);
            return `
              <div class="wx_forecast_day">
                <small>${dayName}</small>
                ${dayIcon}
                <b>${max}°</b>
                <span style="font-size:11px;color:#CFC6B9">${min}°</span>
              </div>
            `;
          }).join('');
        }
      }
    } catch (_) {
      const chip = $('[data-wx-chip]');
      if (chip) chip.innerHTML = `<span>Jaipur · Kukas</span>`;
    }
  };

  loadWeather();

  /* ---------- Instagram Feed Expansion ---------- */
  const igMoreBtn = $('[data-ig-more]');
  igMoreBtn?.addEventListener('click', () => {
    $$('.ig_tile.hide').forEach((tile) => tile.classList.remove('hide'));
    igMoreBtn.style.display = 'none';
  });

  /* ---------- Year stamp ---------- */
  $$('[data-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });
})();
