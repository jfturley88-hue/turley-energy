/* ============================================================
   TURLEY ENERGY CONSULTANTS — main.js
   ============================================================ */

(function () {
  'use strict';

  // === SCROLL-AWARE HEADER ===
  const header = document.getElementById('site-header');
  if (header) {
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 16);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // === MOBILE MENU ===
  const mobileToggle = document.getElementById('mobile-toggle');
  const mainNav      = document.getElementById('main-nav');

  if (mobileToggle && mainNav) {
    mobileToggle.addEventListener('click', () => {
      const open = mainNav.classList.toggle('mobile-open');
      mobileToggle.classList.toggle('open', open);
      mobileToggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (mainNav.classList.contains('mobile-open') &&
          !mainNav.contains(e.target) &&
          !mobileToggle.contains(e.target)) {
        mainNav.classList.remove('mobile-open');
        mobileToggle.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  }

  // === SERVICES DROPDOWN ===
  document.querySelectorAll('.has-dropdown').forEach(item => {
    const btn = item.querySelector('.nav-link');
    let closeTimer = null;

    const cancelClose = () => { if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; } };
    const scheduleClose = () => {
      cancelClose();
      closeTimer = setTimeout(() => closeDropdown(item, btn), 150);
    };

    // Desktop: hover with safe close delay
    item.addEventListener('mouseenter', () => {
      if (window.innerWidth > 768) { cancelClose(); openDropdown(item, btn); }
    });
    item.addEventListener('mouseleave', () => {
      if (window.innerWidth > 768) scheduleClose();
    });

    // Also keep the dropdown open if cursor re-enters the menu itself
    const menu = item.querySelector('.dropdown-menu');
    if (menu) {
      menu.addEventListener('mouseenter', () => { if (window.innerWidth > 768) cancelClose(); });
      menu.addEventListener('mouseleave', () => { if (window.innerWidth > 768) scheduleClose(); });
    }

    // Click: toggle (works on all widths)
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const isOpen = item.classList.contains('open');
      // Close all others first
      document.querySelectorAll('.has-dropdown.open').forEach(other => {
        if (other !== item) closeDropdown(other, other.querySelector('.nav-link'));
      });
      isOpen ? closeDropdown(item, btn) : openDropdown(item, btn);
    });

    // Close on dropdown link click
    item.querySelectorAll('.dropdown-link').forEach(link => {
      link.addEventListener('click', () => { cancelClose(); closeDropdown(item, btn); });
    });
  });

  // Close dropdowns when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.has-dropdown')) {
      document.querySelectorAll('.has-dropdown.open').forEach(item => {
        closeDropdown(item, item.querySelector('.nav-link'));
      });
    }
  });

  // Close mobile nav when any link is clicked
  document.querySelectorAll('#main-nav .dropdown-link, #main-nav .nav-link:not(.has-dropdown .nav-link)').forEach(link => {
    link.addEventListener('click', () => {
      if (mainNav && mainNav.classList.contains('mobile-open')) {
        mainNav.classList.remove('mobile-open');
        if (mobileToggle) {
          mobileToggle.classList.remove('open');
          mobileToggle.setAttribute('aria-expanded', 'false');
        }
        document.body.style.overflow = '';
      }
    });
  });

  function openDropdown(item, btn) {
    item.classList.add('open');
    if (btn) btn.setAttribute('aria-expanded', 'true');
  }

  function closeDropdown(item, btn) {
    item.classList.remove('open');
    if (btn) btn.setAttribute('aria-expanded', 'false');
  }

  // === SMOOTH SCROLL (respects sticky header offset) ===
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const hash   = anchor.getAttribute('href');
      const target = hash && hash !== '#' ? document.querySelector(hash) : null;
      if (!target) return;
      e.preventDefault();
      const headerH = header ? header.offsetHeight : 0;
      const top     = target.getBoundingClientRect().top + window.scrollY - headerH - 12;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  // === CONTACT FORM ===
  const contactForm   = document.getElementById('contact-form');
  const formSuccess   = document.getElementById('form-success');
  const formContainer = document.getElementById('form-container');

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const btn          = contactForm.querySelector('[type="submit"]');
      const originalText = btn.textContent;

      btn.textContent = 'Sending…';
      btn.disabled    = true;

      try {
        // Replace YOUR_FORM_ID with your Formspree form ID
        const res = await fetch('https://formspree.io/f/YOUR_FORM_ID', {
          method:  'POST',
          body:    new FormData(contactForm),
          headers: { 'Accept': 'application/json' }
        });

        if (res.ok) {
          if (formContainer) formContainer.style.display = 'none';
          if (formSuccess)   formSuccess.style.display   = 'block';
        } else {
          throw new Error('Submission failed');
        }
      } catch {
        alert('Something went wrong. Please email us directly at info@turleyenergy.ie');
        btn.textContent = originalText;
        btn.disabled    = false;
      }
    });
  }

})();
