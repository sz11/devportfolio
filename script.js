// Custom cursor
const cursor = document.querySelector('.cursor');
let mouseX = 0, mouseY = 0;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  cursor.style.left = mouseX + 'px';
  cursor.style.top = mouseY + 'px';
});

// Cursor hover effects
document.querySelectorAll('a, button, .project-card, .interest').forEach(el => {
  el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
  el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
});

// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    }
  });
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
const navLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
  if (window.scrollY > 100) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }

  // Update active nav link
  const sections = document.querySelectorAll('section');
  let currentSection = '';

  sections.forEach(section => {
    const sectionTop = section.getBoundingClientRect().top;
    const sectionHeight = section.offsetHeight;
    
    if (sectionTop <= 100 && sectionTop + sectionHeight > 100) {
      currentSection = section.getAttribute('id');
    }
  });

  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === `#${currentSection}`) {
      link.classList.add('active');
    }
  });
});

// Intersection Observer for fade-in animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
  observer.observe(el);
});

// Project cards hover effect with tilt
document.querySelectorAll('.project-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rotateX = (y - centerY) / 10;
    const rotateY = (centerX - x) / 10;
    
    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
  });
  
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
  });
});

// Interest cards staggered animation
const interestCards = document.querySelectorAll('.interest');

const interestObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0px) scale(1)';
      }, index * 100);
    }
  });
}, { threshold: 0.1 });

interestCards.forEach(card => {
  card.style.opacity = '0';
  card.style.transform = 'translateY(30px) scale(0.9)';
  card.style.transition = 'all 0.6s ease';
  interestObserver.observe(card);
});

// Add floating particles effect to hero section
function createParticle() {
  const particle = document.createElement('div');
  particle.style.position = 'absolute';
  particle.style.width = Math.random() * 6 + 2 + 'px';
  particle.style.height = particle.style.width;
  particle.style.background = `rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2})`;
  particle.style.borderRadius = '50%';
  particle.style.left = Math.random() * 100 + '%';
  particle.style.top = '100%';
  particle.style.pointerEvents = 'none';
  particle.style.animation = `floatUp ${Math.random() * 3 + 4}s linear forwards`;
  
  const hero = document.querySelector('.hero');
  hero.appendChild(particle);
  
  setTimeout(() => {
    if (particle.parentNode) {
      particle.parentNode.removeChild(particle);
    }
  }, 7000);
}

// Add CSS for particle animation
const style = document.createElement('style');
style.textContent = `
  @keyframes floatUp {
    to {
      transform: translateY(-100vh) rotate(360deg);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Create particles periodically
setInterval(createParticle, 3000);

// Timeline items animation
const timelineItems = document.querySelectorAll('.timeline-item');
const timelineObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateX(0px)';
      }, index * 200);
    }
  });
}, { threshold: 0.3 });

timelineItems.forEach((item, index) => {
  item.style.opacity = '0';
  item.style.transform = index % 2 === 0 ? 'translateX(-50px)' : 'translateX(50px)';
  item.style.transition = 'all 0.6s ease';
  timelineObserver.observe(item);
});

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
  const sections = ['home', 'about', 'projects', 'experience', 'interests', 'contact'];
  const currentIndex = sections.findIndex(section => {
    const element = document.getElementById(section);
    const rect = element.getBoundingClientRect();
    return rect.top <= 100 && rect.bottom > 100;
  });

  if (e.key === 'ArrowDown' && currentIndex < sections.length - 1) {
    document.getElementById(sections[currentIndex + 1]).scrollIntoView({ behavior: 'smooth' });
  } else if (e.key === 'ArrowUp' && currentIndex > 0) {
    document.getElementById(sections[currentIndex - 1]).scrollIntoView({ behavior: 'smooth' });
  }
});

// Add Go board pattern animation
function animateGoBoard() {
  const hero = document.querySelector('.hero::before');
  if (hero) {
    hero.style.animation = 'none';
    setTimeout(() => {
      hero.style.animation = 'float 20s ease-in-out infinite';
    }, 10);
  }
}

// Performance optimization: throttle scroll events
let ticking = false;
function updateOnScroll() {
  if (!ticking) {
    requestAnimationFrame(() => {
      // Scroll-based animations here
      ticking = false;
    });
    ticking = true;
  }
}

window.addEventListener('scroll', updateOnScroll);

// Preload critical images when they're about to come into view
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      if (img.dataset.src) {
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    }
  });
}, { rootMargin: '50px' });

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Add initial animations
  setTimeout(() => {
    document.querySelector('.hero h1').style.opacity = '1';
    document.querySelector('.hero h2').style.opacity = '1';
  }, 500);
});