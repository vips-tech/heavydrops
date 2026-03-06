const db = require('../config/db');

/**
 * Toggle Like/Unlike
 */
exports.toggleLike = async (req, res) => {
    const { design_id } = req.body;
    const user_id = req.user.id;

    if (!design_id) return res.status(400).json({ error: 'Design ID required' });

    try {
        const existing = await db('likes').where({ user_id, design_id }).first();

        if (existing) {
            await db('likes').where({ like_id: existing.like_id }).del();
            return res.json({ liked: false, message: 'Design unliked' });
        } else {
            await db('likes').insert({ user_id, design_id });
            return res.json({ liked: true, message: 'Design liked' });
        }
    } catch (error) {
        console.error('[LIKE] Toggle failed:', error);
        res.status(500).json({ error: 'Interaction failed' });
    }
};

/**
 * Get Liked Designs for Current User
 */
exports.getLikedDesigns = async (req, res) => {
    try {
        const user_id = req.user.id;
        const designs = await db('likes')
            .join('designs', 'likes.design_id', 'designs.design_id')
            .join('sellers', 'designs.seller_id', 'sellers.seller_id')
            .leftJoin('design_media', function() {
                this.on('designs.design_id', '=', 'design_media.design_id')
                    .andOn('design_media.shot_type', '=', db.raw('?', ['master']))
                    .andOn('design_media.status', '=', db.raw('?', ['approved']))
            })
            .select(
                'designs.*',
                'sellers.business_name',
                'sellers.city',
                'design_media.uri as primary_image_url'
            )
            .where('likes.user_id', user_id)
            .groupBy('designs.design_id');

        const enriched = designs.map(d => ({
            ...d,
            total_price: (d.weight * d.gold_rate_snapshot) + d.making_charge_snapshot
        }));

        res.json(enriched);
    } catch (error) {
        console.error('[LIKES] Failed to fetch likes:', error);
        res.status(500).json({ error: 'Failed to fetch likes' });
    }
};

/**
 * Get Like Status for a Design (Internal for frontend sync)
 */
exports.getLikeStatus = async (req, res) => {
    const { id } = req.params;
    const user_id = req.user.id;

    try {
        const like = await db('likes').where({ user_id, design_id: id }).first();
        res.json({ liked: !!like });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch status' });
    }
};
