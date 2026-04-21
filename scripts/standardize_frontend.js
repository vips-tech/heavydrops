const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, '../public');
const EXCLUDE_FILES = []; // Add filenames if needed

const HEADER_HTML = `
<nav class="std-nav">
    <div class="nav-left">
        <a href="/" style="display: flex; align-items: center; gap: 12px; text-decoration: none;">
            <img src="/assets/logo.png" alt="Heavy Drops">
            <span style="font-family: 'Outfit'; font-weight: 600; font-size: 1.2rem; color: #1a1a1a; letter-spacing: -0.02em;">HEAVY DROPS</span>
        </a>
    </div>
    <div class="nav-center">
        <a href="/">Home</a>
        <a href="/collection">Discover</a>
        <a href="/profile/likes">Liked</a>
    </div>
    <div class="nav-right">
        <div class="nav-auth-channel">
            <!-- Populated by session.js -->
        </div>
    </div>
</nav>
`;

const FOOTER_HTML = `
<footer class="std-footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-col">
                <h4>Platform</h4>
                <ul>
                    <li><a href="/collection">Discover</a></li>
                    <li><a href="/how-it-works">How It Works</a></li>
                    <li><a href="/problem">Problem We Solve</a></li>
                    <li><a href="/philosophy">Philosophy</a></li>
                    <li><a href="/about">About Us</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Legal Protection</h4>
                <ul>
                    <li><a href="/terms">Terms & Conditions</a></li>
                    <li><a href="/wallet-policy">Wallet Policy</a></li>
                    <li><a href="/seller-agreement">Seller Agreement</a></li>
                    <li><a href="/terms#privacy">Privacy Policy</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Partners</h4>
                <ul>
                    <li><a href="/seller-register.html">Become a Seller</a></li>
                    <li><a href="/seller-login">Partner Portal</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Contact</h4>
                <ul>
                    <li><a href="mailto:concierge@heavydrops.com">concierge@heavydrops.com</a></li>
                    <li><span style="opacity: 0.6; font-size: 0.9rem;">Mumbai Only</span></li>
                    <li><span style="opacity: 0.6; font-size: 0.9rem;">+91 98408 28137</span></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 Heavy Drops Intent Network. All rights reserved.</span>
            <span>Est. Mumbai</span>
        </div>
    </div>
</footer>
`;

function processFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');

    // 1. Remove existing Navs and Headers (simplified regex)
    content = content.replace(/<nav[\s\S]*?<\/nav>/gi, '');
    content = content.replace(/<footer[\s\S]*?<\/footer>/gi, '');

    // Also remove any previous session.js script tag to avoid duplication/ordering issues
    content = content.replace(/<script src="\/js\/session.js"><\/script>/gi, '');

    // 2. Inject New Header (After body start)
    // Find body tag
    const bodyMatch = content.match(/<body[^>]*>/i);
    if (bodyMatch) {
        const insertIdx = bodyMatch.index + bodyMatch[0].length;
        content = content.slice(0, insertIdx) + '\n' + HEADER_HTML + content.slice(insertIdx);
    } else {
        console.log(`Skipping ${filePath} (No body tag)`);
        return;
    }

    // 3. Inject New Footer and Script (Before body end)
    const bodyEndMatch = content.match(/<\/body>/i);
    if (bodyEndMatch) {
        const insertIdx = bodyEndMatch.index;
        const closing = `
${FOOTER_HTML}
<script src="/js/session.js"></script>
`;
        content = content.slice(0, insertIdx) + closing + content.slice(insertIdx);
    }

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated: ${filePath}`);
}

fs.readdirSync(PUBLIC_DIR).forEach(file => {
    if (file.endsWith('.html') && !EXCLUDE_FILES.includes(file)) {
        processFile(path.join(PUBLIC_DIR, file));
    }
});
