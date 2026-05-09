/**
 * Heavy Drops - Universal Header Functions
 * Handles gold rate ticker, navigation, and filters across all pages
 */

// Initialize gold rate ticker
async function initGoldRateTicker() {
    try {
        const response = await fetch('/api/health/config');
        const config = await response.json();
        
        if (config && config.gold_rate_22k) {
            const navRight = document.querySelector('.nav-right');
            if (navRight) {
                // Check if ticker already exists
                if (!navRight.querySelector('.gold-rate-ticker')) {
                    const ticker = document.createElement('div');
                    ticker.className = 'gold-rate-ticker';
                    ticker.innerHTML = `
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M12 6v6l4 2"/>
                        </svg>
                        ₹${config.gold_rate_22k.toLocaleString()}/g
                        <span class="rate-label">22K</span>
                    `;
                    // Insert before filter button
                    const filterBtn = navRight.querySelector('.filter-toggle-btn');
                    if (filterBtn) {
                        navRight.insertBefore(ticker, filterBtn);
                    } else {
                        navRight.appendChild(ticker);
                    }
                }
            }
        }
    } catch (error) {
        console.log('Gold rate ticker not available:', error);
    }
}

// Set active navigation link
function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        const linkPath = new URL(link.href).pathname;
        
        // Exact match or home page
        if (currentPath === linkPath) {
            link.classList.add('active');
        }
        // Partial match for nested pages (but not for home)
        else if (linkPath !== '/' && currentPath.includes(linkPath)) {
            link.classList.add('active');
        }
    });
}

// Toggle filter sidebar
function toggleFilters() {
    const sidebar = document.getElementById('filterSidebar');
    const overlay = document.getElementById('filterOverlay');
    
    if (sidebar && overlay) {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        
        if (sidebar.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
}

// Apply filters (calls page-specific fetchDesigns if available)
function applyFilters() {
    if (typeof fetchDesigns === 'function') {
        fetchDesigns();
    } else {
        console.log('Filters applied (no fetchDesigns function on this page)');
    }
}

// Reset all filters
function resetFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const budgetFilter = document.getElementById('budgetFilter');
    const weightFilter = document.getElementById('weightFilter');
    
    if (categoryFilter) categoryFilter.value = '';
    if (budgetFilter) budgetFilter.value = '';
    if (weightFilter) weightFilter.value = '';
    
    applyFilters();
}

// Initialize header on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize gold rate ticker
    initGoldRateTicker();
    
    // Set active navigation link
    setActiveNavLink();
    
    // Close filter sidebar when clicking overlay
    const filterOverlay = document.getElementById('filterOverlay');
    if (filterOverlay) {
        filterOverlay.addEventListener('click', toggleFilters);
    }
    
    // Close filter sidebar when clicking close button
    const filterCloseBtn = document.querySelector('.filter-close-btn');
    if (filterCloseBtn) {
        filterCloseBtn.addEventListener('click', toggleFilters);
    }
});

// Export functions for global use
if (typeof window !== 'undefined') {
    window.toggleFilters = toggleFilters;
    window.applyFilters = applyFilters;
    window.resetFilters = resetFilters;
    window.initGoldRateTicker = initGoldRateTicker;
}
