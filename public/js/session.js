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
        if (!authContainer) return;

        let html = '';

        if (user) {
            if (user.role === 'admin') {
                html += `<a href="/admin.html" class="nav-item">ADMIN</a>`;
            } else if (user.role === 'seller') {
                html += `<a href="/seller-dashboard.html" class="nav-item">DASHBOARD</a>`;
            } else {
                // Buyer - show liked and wallet
                html += `<a href="/profile/likes.html" class="nav-item">LIKED</a>`;
                html += `<a href="/wallet.html" class="nav-item">WALLET</a>`;
            }

            html += `<a href="#" onclick="Session.logout()" class="nav-item">LOGOUT</a>`;
        } else {
            html += `<a href="/login.html" class="nav-item">LOGIN</a>`;
        }

        authContainer.innerHTML = html;

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
