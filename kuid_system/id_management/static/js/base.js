// KU Lost & Found ID System — interactive behaviors

document.addEventListener('DOMContentLoaded', () => {
    /* Fade‑in for page container */
    const container = document.querySelector('.container');
    container?.classList.add('fade-in');

    /* Auto‑dismiss Bootstrap alerts after 4 s */
    document.querySelectorAll('.alert').forEach(alertEl => {
        setTimeout(() => {
            new bootstrap.Alert(alertEl).close();
        }, 4000);
    });

    /* Scroll‑to‑top button */
    initScrollTop();
});

function initScrollTop() {
    const btn = document.createElement('button');
    btn.className = 'scroll-top-btn';
    btn.innerHTML = '▲';
    document.body.appendChild(btn);

    window.addEventListener('scroll', () => {
        if (window.scrollY > 240) {
            btn.style.display = 'block';
            btn.style.opacity = '1';
        } else {
            btn.style.opacity = '0';
            setTimeout(() => (btn.style.display = 'none'), 300);
        }
    });

    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
