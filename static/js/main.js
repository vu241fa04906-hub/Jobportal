(function () {
    'use strict';

    const root = document.documentElement;
    const storedTheme = localStorage.getItem('hirewave-theme');
    if (storedTheme) root.setAttribute('data-theme', storedTheme);

    if (window.AOS) AOS.init({ duration: 700, once: true, offset: 80 });

    const navbar = document.querySelector('.app-navbar');
    const backToTop = document.querySelector('.back-to-top');
    const onScroll = () => {
        const active = window.scrollY > 24;
        navbar?.classList.toggle('nav-scrolled', active);
        backToTop?.classList.toggle('show', window.scrollY > 420);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    document.querySelector('[data-theme-toggle]')?.addEventListener('click', function () {
        const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        localStorage.setItem('hirewave-theme', next);
        this.innerHTML = next === 'dark' ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    });

    backToTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

    document.querySelectorAll('.password-toggle').forEach((button) => {
        button.addEventListener('click', () => {
            const input = button.parentElement.querySelector('.password-input');
            const visible = input.type === 'text';
            input.type = visible ? 'password' : 'text';
            button.innerHTML = visible ? '<i class="fa-solid fa-eye"></i>' : '<i class="fa-solid fa-eye-slash"></i>';
        });
    });

    document.querySelectorAll('.needs-validation').forEach((form) => {
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                const isPostForm = (form.getAttribute('method') || '').toLowerCase() === 'post';
                if (!isPostForm) {
                    event.preventDefault();
                    showToast('Looks good. This frontend is ready for backend form handling.');
                }
            }
            form.classList.add('was-validated');
        });
    });

    document.querySelectorAll('.btn').forEach((button) => {
        button.addEventListener('click', function (event) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${event.clientX - rect.left - size / 2}px`;
            ripple.style.top = `${event.clientY - rect.top - size / 2}px`;
            ripple.className = 'ripple';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    const counters = document.querySelectorAll('[data-counter]');
    const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            const el = entry.target;
            const target = Number(el.dataset.counter);
            const duration = 1200;
            const startTime = performance.now();
            const tick = (now) => {
                const progress = Math.min((now - startTime) / duration, 1);
                el.textContent = Math.floor(progress * target).toLocaleString();
                if (progress < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
            observer.unobserve(el);
        });
    }, { threshold: .35 });
    counters.forEach((counter) => counterObserver.observe(counter));

    const typing = document.querySelector('[data-typing]');
    if (typing) {
        const words = typing.dataset.typing.split(',');
        let wordIndex = 0;
        let charIndex = 0;
        let deleting = false;
        const type = () => {
            const word = words[wordIndex];
            typing.textContent = word.slice(0, charIndex);
            if (!deleting && charIndex < word.length) charIndex += 1;
            else if (deleting && charIndex > 0) charIndex -= 1;
            else if (!deleting) deleting = true;
            else {
                deleting = false;
                wordIndex = (wordIndex + 1) % words.length;
            }
            setTimeout(type, deleting ? 45 : 90);
        };
        type();
    }

    document.querySelectorAll('.password-input').forEach((input) => {
        input.addEventListener('input', () => {
            const meter = document.querySelector('[data-password-strength]');
            if (!meter) return;
            const score = [input.value.length > 7, /[A-Z]/.test(input.value), /\d/.test(input.value), /[^A-Za-z0-9]/.test(input.value)].filter(Boolean).length;
            meter.style.width = `${score * 25}%`;
            meter.style.background = score > 2 ? '#10b981' : score > 1 ? '#f97316' : '#ef4444';
        });
    });

    function showToast(message) {
        const toastEl = document.getElementById('siteToast');
        if (!toastEl || !window.bootstrap) return;
        toastEl.querySelector('.toast-body').textContent = message;
        bootstrap.Toast.getOrCreateInstance(toastEl).show();
    }
})();
