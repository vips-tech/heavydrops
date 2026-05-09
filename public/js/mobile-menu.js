/**
 * Heavy Drops - Universal Mobile Menu Handler
 * Fixes: White bar issues, menu alignment, text visibility
 * Version: 2.0
 */

// Mobile Navigation Toggle
function toggleMobileMenu() {
    const navCenter = document.getElementById('navCenter');
    const body = document.body;
    const isActive = navCenter.classList.contains('active');
    
    if (isActive) {
        navCenter.classList.remove('active');
        body.classList.remove('menu-open');
        body.style.overflow = '';
    } else {
        navCenter.classList.add('active');
        body.classList.add('menu-open');
        body.style.overflow = 'hidden';
    }
}

// Initialize mobile menu handlers when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Close menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-center a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            const navCenter = document.getElementById('navCenter');
            const body = document.body;
            if (navCenter.classList.contains('active')) {
                navCenter.classList.remove('active');
                body.classList.remove('menu-open');
                body.style.overflow = '';
            }
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        const navCenter = document.getElementById('navCenter');
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        
        if (!navCenter || !mobileMenuBtn) return;
        
        const isClickInsideMenu = navCenter.contains(event.target);
        const isClickOnButton = mobileMenuBtn.contains(event.target);
        
        if (!isClickInsideMenu && !isClickOnButton && navCenter.classList.contains('active')) {
            navCenter.classList.remove('active');
            document.body.classList.remove('menu-open');
            document.body.style.overflow = '';
        }
    });

    // Handle window resize - close menu if resizing to desktop
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth > 768) {
                const navCenter = document.getElementById('navCenter');
                if (navCenter && navCenter.classList.contains('active')) {
                    navCenter.classList.remove('active');
                    document.body.classList.remove('menu-open');
                    document.body.style.overflow = '';
                }
            }
        }, 250);
    });

    // Prevent horizontal scroll issues
    document.body.style.overflowX = 'hidden';
    document.documentElement.style.overflowX = 'hidden';
});

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.toggleMobileMenu = toggleMobileMenu;
}
