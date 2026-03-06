const db = require('../config/db');

// Get all curated designs with optional filtering
exports.getCuratedDesigns = async (req, res) => {
    try {
        const { category, occasion, min_price, max_price, min_weight, max_weight } = req.query;

        // 1. Fetch Latest Gold Rates
        const rates = await db('gold_rates').orderBy('updated_at', 'desc');
        const rateMap = rates.reduce((acc, r) => {
            if (!acc[r.purity]) acc[r.purity] = parseFloat(r.rate_per_gram);
            return acc;
        }, { '22K': 6200, '24K': 6800 });

        // First, get the first master image for each design (to avoid duplicates)
        const firstImages = await db('design_media')
            .select('design_id', db.raw('MIN(media_id) as first_media_id'))
            .where({ shot_type: 'master', status: 'approved' })
            .groupBy('design_id');

        const imageMap = {};
        for (const img of firstImages) {
            const media = await db('design_media')
                .where({ media_id: img.first_media_id })
                .first();
            if (media) {
                imageMap[img.design_id] = media.uri;
            }
        }

        // Get like counts separately
        const likeCounts = await db('likes')
            .select('design_id', db.raw('COUNT(*) as likes_count'))
            .groupBy('design_id');
        
        const likeMap = {};
        likeCounts.forEach(l => {
            likeMap[l.design_id] = l.likes_count;
        });

        let query = db('designs')
            .join('sellers', 'designs.seller_id', 'sellers.seller_id')
            .select(
                'designs.*',
                'sellers.business_name',
                'sellers.city',
                'sellers.trust_score'
            )
            .where('availability_status', 'available')
            .where('media_quality_status', 'approved');

        if (category) query = query.where('category', category);
        if (occasion) query = query.where('occasion_tag', occasion);
        if (min_weight) query = query.where('weight', '>=', parseFloat(min_weight));
        if (max_weight) query = query.where('weight', '<=', parseFloat(max_weight));

        const designs = await query;

        // Compute total price display dynamically with GST
        const enrichedDesigns = designs.map(design => {
            const currentRate = rateMap[design.purity] || rateMap['22K'];
            const goldValue = design.weight * currentRate;
            const subtotal = goldValue + design.making_charge_snapshot;
            const gst = subtotal * 0.03;
            const totalPrice = subtotal + gst;

            return {
                ...design,
                name: `${design.purity} Gold ${design.category}`, // Synthesized Name
                seller_name: design.business_name,
                views_count: design.view_count, // Alias to match requirement
                occasion: design.occasion_tag,
                making_charge: design.making_charge_snapshot,
                gold_rate: currentRate,
                current_gold_rate: currentRate, // Keep legacy just in case
                gold_value: goldValue,
                total_price: totalPrice,
                total_price_display: totalPrice,
                gst: gst,
                likes_count: likeMap[design.design_id] || 0,
                primary_image_url: imageMap[design.design_id] || null,
                master_image: imageMap[design.design_id] || null // Keep legacy just in case
            };
        });

        // Backend Budget Filtering (since price is dynamic)
        let filtered = enrichedDesigns;
        if (min_price) filtered = filtered.filter(d => d.total_price >= parseFloat(min_price));
        if (max_price) filtered = filtered.filter(d => d.total_price <= parseFloat(max_price));

        res.json(filtered);
    } catch (error) {
        console.error('[DISCOVERY] Error fetching designs:', error);
        res.status(500).json({ error: 'Failed to fetch curated designs' });
    }
};

// Get design detail by ID
exports.getDesignById = async (req, res) => {
    try {
        const { id } = req.params;

        // 1. Fetch Latest Gold Rates
        const rates = await db('gold_rates').orderBy('updated_at', 'desc');
        const rateMap = rates.reduce((acc, r) => {
            if (!acc[r.purity]) acc[r.purity] = parseFloat(r.rate_per_gram);
            return acc;
        }, { '22K': 6200, '24K': 6800 });

        const design = await db('designs')
            .join('sellers', 'designs.seller_id', 'sellers.seller_id')
            .select(
                'designs.*',
                'sellers.business_name',
                'sellers.city',
                'sellers.trust_score',
                'sellers.seller_id as sid'
            )
            .where('designs.design_id', id)
            .first();

        if (!design) {
            return res.status(404).json({ error: 'Design not found' });
        }

        // Fetch All Approved Media for Gallery
        const media = await db('design_media')
            .where({ design_id: id, status: 'approved' })
            .orderBy('shot_type', 'asc');

        // Increment view count for engagement metrics
        await db('designs').where({ design_id: id }).increment('view_count', 1);

        const currentRate = rateMap[design.purity] || rateMap['22K'];
        const goldValue = design.weight * currentRate;
        const makingCharge = design.making_charge_snapshot;
        const subtotal = goldValue + makingCharge;
        const gst = subtotal * 0.03; // 3% standard jewellery GST
        const totalPrice = subtotal + gst;

        res.json({
            ...design,
            current_gold_rate: currentRate,
            media,
            total_price: totalPrice,
            total_price_display: totalPrice,
            price_breakdown: {
                reference_rate: currentRate,
                weight: design.weight,
                gold_value: goldValue,
                making_charge: makingCharge,
                gst: gst,
                total: totalPrice
            }
        });
    } catch (error) {
        console.error('[DISCOVERY] Error fetching design detail:', error);
        res.status(500).json({ error: 'Failed to fetch design detail' });
    }
};
