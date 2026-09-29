// Settings Menu Toggle
function toggleSettingsMenu() {
    const menu = document.getElementById('settingsMenu');
    menu.classList.toggle('active');
}

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.querySelector('.settings-dropdown');
    if (dropdown && !dropdown.contains(e.target)) {
        const menu = document.getElementById('settingsMenu');
        if (menu) menu.classList.remove('active');
    }
});

// Language Switcher
function setLanguage(lang) {
    fetch(`/set_language/${lang}`)
        .then(() => window.location.reload());
}

// Scroll Reveal Animation
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    document.querySelectorAll('.reveal').forEach(el => {
        observer.observe(el);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initScrollReveal();
});

// Navbar background on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(10, 10, 10, 0.95)';
    } else {
        navbar.style.background = 'rgba(10, 10, 10, 0.85)';
    }
});