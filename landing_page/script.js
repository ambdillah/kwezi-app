// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Mobile menu toggle (if needed)
const navToggle = document.createElement('button');
navToggle.className = 'nav-toggle';
navToggle.innerHTML = '☰';
navToggle.style.display = 'none';

const navbar = document.querySelector('.navbar .container');
const navLinks = document.querySelector('.nav-links');

if (window.innerWidth <= 768) {
    navbar.insertBefore(navToggle, navLinks);
    navToggle.style.display = 'block';
    navToggle.style.background = 'none';
    navToggle.style.border = 'none';
    navToggle.style.fontSize = '1.5rem';
    navToggle.style.cursor = 'pointer';
    navToggle.style.color = 'var(--primary-color)';
    
    navToggle.addEventListener('click', () => {
        navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        if (navLinks.style.display === 'flex') {
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '60px';
            navLinks.style.right = '20px';
            navLinks.style.background = 'white';
            navLinks.style.padding = '1rem';
            navLinks.style.borderRadius = '0.5rem';
            navLinks.style.boxShadow = 'var(--shadow-lg)';
        }
    });
}

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards and game cards
document.querySelectorAll('.feature-card, .game-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Update current year in footer
const currentYear = new Date().getFullYear();
const footerText = document.querySelector('.footer-bottom p');
if (footerText) {
    footerText.textContent = `© ${currentYear} Kwezi. Tous droits réservés.`;
}

// Add active state to navigation links
const sections = document.querySelectorAll('section[id]');
const navItems = document.querySelectorAll('.nav-links a');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });

    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href') === `#${current}`) {
            item.classList.add('active');
        }
    });
});

// Console message
console.log('%cKwezi 🏝️', 'font-size: 24px; font-weight: bold; color: #2563eb;');
console.log('%cApprends le Shimaoré et le Kibouchi', 'font-size: 14px; color: #6b7280;');
console.log('https://mayotte-learn-4.preview.emergentagent.com');
