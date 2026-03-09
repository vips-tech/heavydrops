/**
 * User Session Management Utilities
 */

// STATEFUL ENVIRONMENT GUARD
if (window.location.protocol === 'file:') {
    alert('APP RUNNING IN STATIC MODE: Heavy Drops requires a routed backend environment. Please visit http://localhost:5001 instead of opening files directly.');
    console.error('SYSTEM ERROR: Platform requires Stateful Application Mode. Backend disconnected.');
}

const Session = {
    getToken: () => localStorage.getItem('token'),
    setToken: (token) => localStorage.setItem('token', token),
    clearToken: () => localStorage.removeItem('token'),

    isAuthenticated: () => !!localStorage.getItem('token'),

    getUser: async () => {
        const token = Session.getToken();
        if (!token) return null;

        const response = await fetch('/api/auth/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) return await response.json();
        Session.clearToken();
        return null;
    },

    updateNav: async () => {
        const user = await Session.getUser();
        const authContainer = document.querySelector('.nav-auth-channel');
        const navCenter = document.getElementById('navCenter');
        
        if (!authContainer) return;

        let html = '';
        let mobileAuthHtml = '';

        if (user) {
            if (user.role === 'admin') {
                html += `<a href="/admin" class="nav-item">ADMIN</a>`;
                mobileAuthHtml += `<a href="/admin" class="mobile-auth-link">ADMIN</a>`;
            } else if (user.role === 'seller') {
                html += `<a href="/seller-dashboard" class="nav-item">DASHBOARD</a>`;
                mobileAuthHtml += `<a href="/seller-dashboard" class="mobile-auth-link">DASHBOARD</a>`;
            } else {
                // Buyer - show liked and wallet
                html += `<a href="/profile/likes" class="nav-item">LIKED</a>`;
                html += `<a href="/wallet" class="nav-item">WALLET</a>`;
                mobileAuthHtml += `<a href="/profile/likes" class="mobile-auth-link">LIKED</a>`;
                mobileAuthHtml += `<a href="/wallet" class="mobile-auth-link">WALLET</a>`;
            }

            html += `<a href="#" onclick="Session.logout()" class="nav-item">LOGOUT</a>`;
            mobileAuthHtml += `<a href="#" onclick="Session.logout()" class="mobile-auth-link">LOGOUT</a>`;
        } else {
            html += `<a href="/login" class="nav-item">LOGIN</a>`;
            mobileAuthHtml += `<a href="/login" class="mobile-auth-link">LOGIN</a>`;
        }

        authContainer.innerHTML = html;

        // Add mobile auth links to nav-center if it exists
        if (navCenter) {
            // Remove existing mobile auth links
            navCenter.querySelectorAll('.mobile-auth-link').forEach(link => link.remove());
            // Add new mobile auth links
            navCenter.insertAdjacentHTML('beforeend', mobileAuthHtml);
        }

        // Highlight active link
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-center a, .nav-auth-channel a').forEach(link => {
            const href = link.getAttribute('href');
            if (href && href !== '#' && (href === currentPath || currentPath.startsWith(href))) {
                link.classList.add('active');
            }
        });
    },

    logout: () => {
        Session.clearToken();
        window.location.href = '/login';
    }
};

// Auto-run on load
document.addEventListener('DOMContentLoaded', () => {
    Session.updateNav();
});
window.Session = Session;

// Mobile menu toggle function (available globally)
window.toggleMobileMenu = function() {
    const navCenter = document.getElementById('navCenter');
    if (navCenter) {
        navCenter.classList.toggle('active');
    }
};
