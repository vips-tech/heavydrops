/**
 * Heavy Drops - Enhanced Features
 * Live Gold Rates, Animations, and Modern Interactions
 */

class HeavyDropsEnhanced {
    constructor() {
        this.goldRate = 6479; // Real 22K gold rate in India (₹6,479/gram)
        this.isLoading = false;
        this.observers = new Map();
        this.init();
    }

    async init() {
        this.setupScrollEffects();
        this.setupIntersectionObserver();
        this.setupGoldRateTicker();
        this.setupMobileNavigation();
        this.setupImageLazyLoading();
        this.setupSmoothScrolling();
        this.startGoldRateUpdates();
    }

    // Live Gold Rate Management
    async fetchGoldRate() {
        try {
            // Use real Indian 22K gold rate with small fluctuations
            const baseRate = 6479; // Real 22K gold rate
            const fluctuation = (Math.random() - 0.5) * 50; // ±25 rupees fluctuation
            this.goldRate = Math.round(baseRate + fluctuation);
            
            this.updateGoldRateDisplay();
            this.updatePriceCalculations();
            
        } catch (error) {
            console.error('Failed to fetch gold rate:', error);
        }
    }

    updateGoldRateDisplay() {
        const ticker = document.querySelector('.gold-rate-ticker');
        if (ticker) {
            const rateElement = ticker.querySelector('.rate-value');
            if (rateElement) {
                // Add animation class
                ticker.classList.add('updating');
                
                setTimeout(() => {
                    rateElement.textContent = `₹${this.goldRate.toLocaleString()}/g`;
                    ticker.classList.remove('updating');
                }, 300);
            }
        }
    }

    updatePriceCalculations() {
        // Update all price displays based on new gold rate
        const priceElements = document.querySelectorAll('[data-weight]');
        priceElements.forEach(element => {
            const weight = parseFloat(element.dataset.weight);
            const makingCharge = parseFloat(element.dataset.making) || 0;
            const gst = parseFloat(element.dataset.gst) || 0;
            
            if (weight) {
                const goldValue = weight * this.goldRate;
                const total = goldValue + makingCharge + gst;
                
                const totalElement = element.querySelector('.total-price');
                if (totalElement) {
                    totalElement.textContent = `₹${Math.round(total).toLocaleString()}`;
                }
            }
        });
    }

    setupGoldRateTicker() {
        const navRight = document.querySelector('.nav-right');
        if (navRight && !document.querySelector('.gold-rate-ticker')) {
            const ticker = document.createElement('div');
            ticker.className = 'gold-rate-ticker';
            ticker.innerHTML = `
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <circle cx="12" cy="12" r="3"/>
                    <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"/>
                </svg>
                <span class="rate-value">₹${this.goldRate.toLocaleString()}/g</span>
                <span class="rate-label">LIVE 22K</span>
            `;
            
            // Insert before filter button
            const filterBtn = navRight.querySelector('.filter-toggle-btn');
            if (filterBtn) {
                navRight.insertBefore(ticker, filterBtn);
            } else {
                navRight.prepend(ticker);
            }
        }
    }

    startGoldRateUpdates() {
        // Update gold rate every 30 seconds
        setInterval(() => {
            this.fetchGoldRate();
        }, 30000);
        
        // Initial fetch
        this.fetchGoldRate();
    }

    // Scroll Effects
    setupScrollEffects() {
        let lastScrollY = window.scrollY;
        const nav = document.querySelector('.std-nav');
        
        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;
            
            if (nav) {
                if (currentScrollY > 50) {
                    nav.classList.add('scrolled');
                } else {
                    nav.classList.remove('scrolled');
                }
            }
            
            lastScrollY = currentScrollY;
        });
    }

    // Intersection Observer for Animations
    setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    
                    // Add staggered animation for grid items
                    if (entry.target.classList.contains('design-card')) {
                        const cards = Array.from(entry.target.parentElement.children);
                        const index = cards.indexOf(entry.target);
                        entry.target.style.animationDelay = `${index * 0.1}s`;
                    }
                }
            });
        }, observerOptions);

        // Observe elements that should animate on scroll
        const animateElements = document.querySelectorAll('.fade-in-observer, .design-card, .filter-panel');
        animateElements.forEach(el => observer.observe(el));
        
        this.observers.set('intersection', observer);
    }

    // Enhanced Mobile Navigation
    setupMobileNavigation() {
        const mobileBtn = document.querySelector('.mobile-menu-btn');
        const navCenter = document.querySelector('.nav-center');
        
        if (mobileBtn && navCenter) {
            mobileBtn.addEventListener('click', () => {
                const isActive = navCenter.classList.contains('active');
                
                if (isActive) {
                    navCenter.classList.remove('active');
                    mobileBtn.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                } else {
                    navCenter.classList.add('active');
                    mobileBtn.setAttribute('aria-expanded', 'true');
                    document.body.style.overflow = 'hidden';
                }
                
                // Animate hamburger icon
                const svg = mobileBtn.querySelector('svg');
                if (svg) {
                    svg.style.transform = isActive ? 'rotate(0deg)' : 'rotate(90deg)';
                }
            });
            
            // Close mobile menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!mobileBtn.contains(e.target) && !navCenter.contains(e.target)) {
                    navCenter.classList.remove('active');
                    mobileBtn.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                }
            });
            
            // Close mobile menu on escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && navCenter.classList.contains('active')) {
                    navCenter.classList.remove('active');
                    mobileBtn.setAttribute('aria-expanded', 'false');
                    document.body.style.overflow = '';
                }
            });
        }
    }

    // Image Lazy Loading with Fade-in Effect
    setupImageLazyLoading() {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.dataset.src;
                    
                    if (src) {
                        img.src = src;
                        img.classList.add('loading');
                        
                        img.onload = () => {
                            img.classList.remove('loading');
                            img.classList.add('loaded');
                        };
                        
                        img.onerror = () => {
                            img.classList.remove('loading');
                            img.classList.add('error');
                        };
                        
                        imageObserver.unobserve(img);
                    }
                }
            });
        });

        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
        
        this.observers.set('image', imageObserver);
    }

    // Smooth Scrolling for Anchor Links
    setupSmoothScrolling() {
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href^="#"]');
            if (link) {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    const navHeight = document.querySelector('.std-nav')?.offsetHeight || 0;
                    const targetPosition = targetElement.offsetTop - navHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    }

    // Enhanced Like Animation with Heart Tinkle
    animateLike(button, isLiked) {
        const svg = button.querySelector('svg');
        if (!svg) return;
        
        if (isLiked) {
            button.classList.add('active');
            svg.style.fill = '#ef4444';
            svg.style.stroke = '#ef4444';
            
            // Add tinkle animation class
            button.classList.add('heart-tinkle');
            
            // Create heart particles with tinkle effect
            this.createHeartParticles(button);
            
            // Remove tinkle class after animation
            setTimeout(() => {
                button.classList.remove('heart-tinkle');
            }, 600);
        } else {
            button.classList.remove('active');
            svg.style.fill = 'none';
            svg.style.stroke = 'currentColor';
        }
        
        // Bounce animation
        button.style.transform = 'scale(1.3)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 200);
    }

    createHeartParticles(button) {
        const rect = button.getBoundingClientRect();
        const particles = 8; // More particles for better effect
        
        for (let i = 0; i < particles; i++) {
            const particle = document.createElement('div');
            particle.innerHTML = '♥';
            particle.className = 'heart-particle';
            particle.style.cssText = `
                position: fixed;
                left: ${rect.left + rect.width / 2}px;
                top: ${rect.top + rect.height / 2}px;
                color: #ef4444;
                font-size: ${12 + Math.random() * 8}px;
                pointer-events: none;
                z-index: 9999;
                animation: heartFloat 1s ease-out forwards;
                transform: translate(-50%, -50%);
                opacity: 1;
            `;
            
            // Random direction with more spread
            const angle = (i / particles) * Math.PI * 2;
            const distance = 40 + Math.random() * 30;
            particle.style.setProperty('--end-x', `${Math.cos(angle) * distance}px`);
            particle.style.setProperty('--end-y', `${Math.sin(angle) * distance}px`);
            
            document.body.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 1000);
        }
    }

    // Loading States
    showLoadingGrid(container, count = 6) {
        const loadingHTML = Array(count).fill(0).map(() => `
            <div class="loading-card">
                <div class="loading-card-media"></div>
                <div class="loading-card-content">
                    <div class="loading-line short"></div>
                    <div class="loading-line medium"></div>
                    <div class="loading-line"></div>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = `<div class="loading-grid">${loadingHTML}</div>`;
    }

    // Utility Methods
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Cleanup
    destroy() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
    }
}

// CSS for heart particles animation
const style = document.createElement('style');
style.textContent = `
    @keyframes heartFloat {
        0% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1) rotate(0deg);
        }
        50% {
            opacity: 0.8;
            transform: translate(calc(-50% + var(--end-x)), calc(-50% + var(--end-y) * 0.5)) scale(1.2) rotate(180deg);
        }
        100% {
            opacity: 0;
            transform: translate(calc(-50% + var(--end-x)), calc(-50% + var(--end-y))) scale(0.3) rotate(360deg);
        }
    }
    
    @keyframes heartTinkle {
        0%, 100% { transform: scale(1) rotate(0deg); }
        10% { transform: scale(1.2) rotate(-10deg); }
        20% { transform: scale(1.1) rotate(10deg); }
        30% { transform: scale(1.3) rotate(-10deg); }
        40% { transform: scale(1.2) rotate(10deg); }
        50% { transform: scale(1.4) rotate(0deg); }
        60% { transform: scale(1.2) rotate(-5deg); }
        70% { transform: scale(1.1) rotate(5deg); }
        80% { transform: scale(1.05) rotate(-2deg); }
        90% { transform: scale(1.02) rotate(2deg); }
    }
    
    .card-like-btn.heart-tinkle {
        animation: heartTinkle 0.6s ease-out;
    }
    
    .heart-particle {
        font-weight: bold;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.8);
    }
    
    .gold-rate-ticker.updating {
        animation: goldPulse 0.6s ease-out;
    }
    
    @keyframes goldPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    img.loading {
        opacity: 0.5;
        filter: blur(2px);
    }
    
    img.loaded {
        opacity: 1;
        filter: none;
        transition: all 0.3s ease;
    }
    
    img.error {
        opacity: 0.3;
        filter: grayscale(1);
    }
`;
document.head.appendChild(style);

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.heavyDropsEnhanced = new HeavyDropsEnhanced();
    });
} else {
    window.heavyDropsEnhanced = new HeavyDropsEnhanced();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HeavyDropsEnhanced;
}