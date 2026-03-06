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
        // Target specifically the right-side auth container
        const authContainer = document.querySelector('.nav-auth-channel');
        if (!authContainer) return;

        let html = '';

        if (user) {
            html += `<a href="/wallet" class="nav-item">Wallet</a>`;

            // Logic for "Book a Visit" is context dependent (active blocks), 
            // but for global header we can show "Intent Path" if relevant or keep it clean.
            // Requirement: "Book a Visit (if blocked design exists)" -> This requires fetching state.
            // For MVP simplicity in header, we can link to Intent Path if authenticated.

            if (user.role === 'admin') {
                html += `<a href="/admin" class="nav-item highlight">Admin</a>`;
            } else if (user.role === 'seller') {
                html += `<a href="/seller-dashboard" class="nav-item highlight">Dashboard</a>`;
            } else {
                // Buyer
                html += `<a href="/profile/likes" class="nav-item">Profile</a>`;
            }

            html += `<a href="#" onclick="Session.logout()" class="nav-item">Logout</a>`;
        } else {
            // Seller login must NOT mix with buyer login publicly in nav as per requirement "Seller login must NOT mix"
            // But usually a generic Login leads to role selection or separate link.
            // Requirement: "Login / Profile"
            html += `<a href="/login" class="nav-item">Login</a>`;
        }

        authContainer.innerHTML = html;

        // Also highlight active center link
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-center a').forEach(link => {
            if (link.getAttribute('href') === currentPath) link.classList.add('active');
        });
    },

    logout: () => {
        Session.clearToken();
        window.location.href = '/login';
    }
};

// Auto-run on load
document.addEventListener('DOMContentLoaded', Session.updateNav);
window.Session = Session;
