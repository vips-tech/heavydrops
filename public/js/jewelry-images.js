/**
 * Unique Jewelry Images Collection
 * Using Unsplash with specific jewelry queries for real images
 */

const JewelryImages = {
    // Necklace Images - Real gold necklace photos
    necklaces: [
        'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=600&h=600&fit=crop&q=80'
    ],
    
    // Ring Images - Real gold ring photos
    rings: [
        'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1603561596112-0a132b757442?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1614170143028-a2e6d4c6e0f7?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1588444650700-c5886c00c0e9?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1590858593969-a0e561f5e4e3?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1611955167811-4711904bb9f8?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600&h=600&fit=crop&q=80'
    ],
    
    // Bangle Images - Real gold bangle/bracelet photos
    bangles: [
        'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?w=600&h=600&fit=crop&q=80'
    ],
    
    // Earring Images - Real gold earring photos
    earrings: [
        'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?w=600&h=600&fit=crop&q=80'
    ],
    
    // Bracelet Images - Real gold bracelet photos
    bracelets: [
        'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?w=600&h=600&fit=crop&q=80'
    ],

    // Default fallback images
    default: [
        'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&h=600&fit=crop&q=80',
        'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=600&h=600&fit=crop&q=80'
    ],

    // Get unique image for a design based on category
    getUniqueImage(category, designId) {
        console.log('[JewelryImages] Getting image for:', { category, designId });
        
        if (!category) {
            console.warn('[JewelryImages] No category provided, using default');
            return this.default[0];
        }
        
        // Normalize category name to match our keys
        const categoryMap = {
            'necklace': 'necklaces',
            'necklaces': 'necklaces',
            'ring': 'rings',
            'rings': 'rings',
            'bangle': 'bangles',
            'bangles': 'bangles',
            'earring': 'earrings',
            'earrings': 'earrings',
            'bracelet': 'bracelets',
            'bracelets': 'bracelets'
        };
        
        const normalizedCategory = categoryMap[category.toLowerCase()];
        
        if (!normalizedCategory) {
            console.warn('[JewelryImages] Unknown category:', category, '- using default');
            return this.default[0];
        }
        
        const images = this[normalizedCategory];
        
        if (!images || images.length === 0) {
            console.warn('[JewelryImages] No images for category:', normalizedCategory);
            return this.default[0];
        }
        
        // Use design ID to consistently select the same image for the same design
        const index = (designId * 7 + Math.floor(designId / 3)) % images.length;
        const selectedImage = images[index];
        
        console.log('[JewelryImages] Selected:', { 
            category, 
            normalizedCategory, 
            index, 
            totalImages: images.length,
            image: selectedImage 
        });
        
        return selectedImage;
    },

    // Get multiple images for a design (for gallery)
    getDesignGallery(category, designId, count = 4) {
        const categoryMap = {
            'necklace': 'necklaces',
            'necklaces': 'necklaces',
            'ring': 'rings',
            'rings': 'rings',
            'bangle': 'bangles',
            'bangles': 'bangles',
            'earring': 'earrings',
            'earrings': 'earrings',
            'bracelet': 'bracelets',
            'bracelets': 'bracelets'
        };
        
        const normalizedCategory = categoryMap[category.toLowerCase()] || 'default';
        const images = this[normalizedCategory] || this.default;
        
        const gallery = [];
        for (let i = 0; i < count; i++) {
            const index = (designId * 7 + i * 3) % images.length;
            gallery.push(images[index]);
        }
        
        return gallery;
    },

    // Get hero background images
    getHeroImages() {
        return [
            'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=2070&h=800&fit=crop&q=80',
            'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=2070&h=800&fit=crop&q=80',
            'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=2070&h=800&fit=crop&q=80',
            'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=2070&h=800&fit=crop&q=80'
        ];
    },

    // Preload images for better performance
    preloadImages(category = null) {
        const imagesToPreload = category ? 
            (this[category.toLowerCase() + 's'] || this.default) : 
            [...this.necklaces, ...this.rings, ...this.bangles, ...this.earrings].slice(0, 30);

        imagesToPreload.forEach(src => {
            const img = new Image();
            img.src = src;
        });
    }
};

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.JewelryImages = JewelryImages;
    console.log('[JewelryImages] Module loaded successfully with', {
        necklaces: JewelryImages.necklaces.length,
        rings: JewelryImages.rings.length,
        bangles: JewelryImages.bangles.length,
        earrings: JewelryImages.earrings.length,
        bracelets: JewelryImages.bracelets.length
    }, 'images per category');
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = JewelryImages;
}
