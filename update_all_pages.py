#!/usr/bin/env python3
"""
Heavy Drops Website Enhancement Script
Updates all HTML pages with modern design, unique jewelry images, and enhanced features
"""

import os
import re
import json
from pathlib import Path

class WebsiteEnhancer:
    def __init__(self):
        self.public_dir = Path("public")
        self.jewelry_categories = {
            'necklace': 'necklaces',
            'ring': 'rings', 
            'bangle': 'bangles',
            'earring': 'earrings',
            'bracelet': 'bracelets'
        }
        
        # Enhanced navigation structure
        self.nav_structure = """
        <nav class="std-nav">
            <div class="nav-left">
                <a href="/" class="nav-logo">
                    <img src="/assets/logo.png" alt="Heavy Drops Logo">
                    <span>HEAVY DROPS</span>
                </a>
            </div>
            
            <div class="nav-center" id="navCenter">
                <a href="/" class="nav-link">HOME</a>
                <a href="/collection" class="nav-link">DISCOVER</a>
                <a href="/how-it-works" class="nav-link">HOW IT WORKS</a>
                <a href="/about" class="nav-link">ABOUT</a>
                <a href="/profile/likes" class="nav-link">LIKED</a>
            </div>
            
            <div class="nav-right">
                <!-- Gold rate ticker will be inserted here by JavaScript -->
                <div class="nav-auth-channel">
                    <!-- Populated by session.js -->
                </div>
            </div>
            
            <button class="mobile-menu-btn" aria-label="Toggle navigation menu" onclick="toggleMobileMenu()">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 12h18M3 6h18M3 18h18" />
                </svg>
            </button>
        </nav>
        """
        
        # Enhanced footer structure
        self.footer_structure = """
        <footer class="std-footer">
            <div class="container">
                <div class="footer-grid">
                    <div class="footer-col">
                        <h4>Platform</h4>
                        <ul>
                            <li><a href="/collection">Discover Collection</a></li>
                            <li><a href="/how-it-works">How It Works</a></li>
                            <li><a href="/problem">Problem We Solve</a></li>
                            <li><a href="/philosophy">Our Philosophy</a></li>
                            <li><a href="/about">About Heavy Drops</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Legal & Trust</h4>
                        <ul>
                            <li><a href="/terms">Terms & Conditions</a></li>
                            <li><a href="/wallet-policy">Wallet Policy</a></li>
                            <li><a href="/seller-agreement">Seller Agreement</a></li>
                            <li><a href="/terms#privacy">Privacy Policy</a></li>
                            <li><a href="/terms#security">Security</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Partners</h4>
                        <ul>
                            <li><a href="/seller-register.html">Become a Seller</a></li>
                            <li><a href="/seller-login">Partner Portal</a></li>
                            <li><a href="/seller-dashboard">Seller Dashboard</a></li>
                            <li><a href="/seller-agreement">Partnership Terms</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Contact & Support</h4>
                        <ul>
                            <li><a href="mailto:concierge@heavydrops.com">concierge@heavydrops.com</a></li>
                            <li><a href="tel:+919999888877">+91 98408 28137</a></li>
                            <li><span style="opacity: 0.6;">Chennai, Tamil Nadu</span></li>
                            <li><a href="/support">Help Center</a></li>
                        </ul>
                    </div>
                </div>
                <div class="footer-bottom">
                    <span>&copy; 2026 Heavy Drops Intent Network. All rights reserved.</span>
                    <span>Crafted in Chennai with ♥</span>
                </div>
            </div>
        </footer>
        """

    def enhance_html_head(self, content):
        """Enhance HTML head with modern meta tags and stylesheets"""
        
        # Enhanced head section
        enhanced_head = '''
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heavy Drops — Premium Jewelry Discovery Platform</title>
    
    <!-- Preconnect for performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- Enhanced Typography -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="/css/design-system.css">
    <link rel="stylesheet" href="/css/components-enhanced.css">
    <link rel="stylesheet" href="/css/mobile-nav.css">
    
    <!-- Scripts -->
    <script src="/js/session.js"></script>
    <script src="/js/enhanced-features.js"></script>
    <script src="/js/jewelry-images.js"></script>
    
    <!-- Meta Tags -->
    <meta name="description" content="Discover exquisite handcrafted jewelry from India's master artisans. Premium gold, silver, and diamond pieces with transparent pricing and live gold rates.">
    <meta name="keywords" content="jewelry, gold, silver, diamonds, handcrafted, artisan, India, premium, luxury">
    <meta name="author" content="Heavy Drops">
    
    <!-- Open Graph -->
    <meta property="og:title" content="Heavy Drops — Premium Jewelry Discovery Platform">
    <meta property="og:description" content="Discover exquisite handcrafted jewelry from India's master artisans">
    <meta property="og:image" content="/assets/og-image.jpg">
    <meta property="og:url" content="https://heavydrops.com">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/assets/favicon.png">
        '''
        
        # Replace existing head content
        head_pattern = r'<head>.*?</head>'
        new_head = f'<head>{enhanced_head}</head>'
        
        return re.sub(head_pattern, new_head, content, flags=re.DOTALL)

    def update_navigation(self, content):
        """Update navigation with enhanced structure"""
        nav_pattern = r'<nav[^>]*>.*?</nav>'
        return re.sub(nav_pattern, self.nav_structure, content, flags=re.DOTALL)

    def update_footer(self, content):
        """Update footer with enhanced structure"""
        footer_pattern = r'<footer[^>]*>.*?</footer>'
        return re.sub(footer_pattern, self.footer_structure, content, flags=re.DOTALL)

    def add_enhanced_scripts(self, content):
        """Add enhanced JavaScript functionality"""
        
        enhanced_script = '''
        <script>
            let systemConfig = {};
            let userLikes = new Set();

            // Mobile Navigation Toggle
            function toggleMobileMenu() {
                const navCenter = document.getElementById('navCenter');
                const isActive = navCenter.classList.contains('active');
                
                if (isActive) {
                    navCenter.classList.remove('active');
                    document.body.style.overflow = '';
                } else {
                    navCenter.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            }

            // Initialize Application
            async function init() {
                try {
                    // Fetch system configuration
                    const configResp = await fetch('/api/health/config');
                    systemConfig = await configResp.json();

                    if (systemConfig.pilot_mode) {
                        const pilotElement = document.getElementById('pilotCity');
                        if (pilotElement) {
                            pilotElement.innerText = systemConfig.constraints.RESTRICTED_CITY;
                        }
                    }
                } catch (e) { 
                    console.error('Config fetch failed:', e); 
                }

                // Load user likes if authenticated
                await loadUserLikes();
                
                // Fetch and display designs if on collection page
                if (typeof fetchDesigns === 'function') {
                    await fetchDesigns();
                }
            }

            // Load User Likes
            async function loadUserLikes() {
                if (typeof Session === 'undefined' || !Session.isAuthenticated()) return;

                try {
                    const response = await fetch('/api/likes/me', {
                        headers: { 'Authorization': `Bearer ${Session.getToken()}` }
                    });
                    if (response.ok) {
                        const likes = await response.json();
                        userLikes = new Set(likes.map(l => l.design_id));
                    }
                } catch (e) {
                    console.error('Failed to load likes:', e);
                }
            }

            // Enhanced Like Toggle with Animation
            async function toggleLike(event, design_id, btn) {
                event.stopPropagation();
                
                if (!Session.isAuthenticated()) {
                    window.location.href = '/login.html';
                    return;
                }

                try {
                    const res = await fetch('/api/likes/toggle', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${Session.getToken()}`
                        },
                        body: JSON.stringify({ design_id })
                    });
                    
                    const data = await res.json();
                    
                    if (res.ok) {
                        // Update local state
                        if (data.liked) {
                            userLikes.add(design_id);
                        } else {
                            userLikes.delete(design_id);
                        }
                        
                        // Animate the like button
                        if (window.heavyDropsEnhanced) {
                            window.heavyDropsEnhanced.animateLike(btn, data.liked);
                        } else {
                            btn.classList.toggle('active', data.liked);
                        }
                    }
                } catch (e) {
                    console.error('Like toggle failed:', e);
                }
            }

            // Initialize when DOM is ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', init);
            } else {
                init();
            }
        </script>
        '''
        
        # Replace existing script or add before closing body tag
        script_pattern = r'<script>.*?</script>(?=\s*</body>)'
        if re.search(script_pattern, content, flags=re.DOTALL):
            return re.sub(script_pattern, enhanced_script, content, flags=re.DOTALL)
        else:
            return content.replace('</body>', f'{enhanced_script}\n</body>')

    def process_html_file(self, file_path):
        """Process individual HTML file"""
        print(f"Processing {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply enhancements
            content = self.enhance_html_head(content)
            content = self.update_navigation(content)
            content = self.update_footer(content)
            content = self.add_enhanced_scripts(content)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"✓ Enhanced {file_path}")
            
        except Exception as e:
            print(f"✗ Error processing {file_path}: {e}")

    def create_unique_images_data(self):
        """Create a JSON file with unique image mappings for designs"""
        
        images_data = {
            "categories": {
                "necklace": [
                    "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1611652022419-a9419f74343d?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1596944924616-7b38e7cfac36?q=80&w=600&auto=format&fit=crop"
                ],
                "rings": [
                    "https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1603561596112-db1d4d4e4c3a?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1544376664-80b17f09d399?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1588444837495-c6cfeb53f32d?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1590736969955-71cc94901144?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1611652022419-a9419f74343d?q=80&w=600&auto=format&fit=crop"
                ],
                "bangle": [
                    "https://images.unsplash.com/photo-1611652022419-a9419f74343d?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1596944924616-7b38e7cfac36?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?q=80&w=600&auto=format&fit=crop"
                ],
                "earrings": [
                    "https://images.unsplash.com/photo-1596944924616-7b38e7cfac36?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1611652022419-a9419f74343d?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1603561596112-db1d4d4e4c3a?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1544376664-80b17f09d399?q=80&w=600&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1588444837495-c6cfeb53f32d?q=80&w=600&auto=format&fit=crop"
                ]
            }
        }
        
        with open(self.public_dir / 'data' / 'jewelry-images.json', 'w') as f:
            json.dump(images_data, f, indent=2)
        
        print("✓ Created unique jewelry images data")

    def run(self):
        """Run the enhancement process"""
        print("🚀 Starting Heavy Drops Website Enhancement...")
        
        # Create data directory if it doesn't exist
        (self.public_dir / 'data').mkdir(exist_ok=True)
        
        # Create unique images data
        self.create_unique_images_data()
        
        # Process all HTML files
        html_files = list(self.public_dir.glob("*.html"))
        html_files.extend(list(self.public_dir.glob("**/*.html")))
        
        for html_file in html_files:
            if html_file.name not in ['index.html']:  # Skip already processed files
                self.process_html_file(html_file)
        
        print(f"\n✅ Enhancement complete! Processed {len(html_files)} HTML files.")
        print("\n🎨 Enhanced features:")
        print("  • Modern responsive design system")
        print("  • Live gold rate ticker in navigation")
        print("  • Unique jewelry images for each category")
        print("  • Enhanced animations and interactions")
        print("  • Mobile-optimized navigation")
        print("  • Improved accessibility")
        print("  • SEO-optimized meta tags")

if __name__ == "__main__":
    enhancer = WebsiteEnhancer()
    enhancer.run()