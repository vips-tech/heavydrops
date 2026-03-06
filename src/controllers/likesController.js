const db = require('../config/db');

exports.toggleLike = async (req, res) => {
    try {
        const user_id = req.user.id;
        const { design_id } = req.body;

        const existingLike = await db('likes').where({ user_id, design_id }).first();

        if (existingLike) {
            await db('likes').where({ user_id, design_id }).del();
            return res.json({ message: 'Unliked', liked: false });
        } else {
            await db('likes').insert({ user_id, design_id });
            return res.json({ message: 'Liked', liked: true });
        }
    } catch (error) {
        console.error('Error in toggleLike:', error);
        res.status(500).json({ error: 'Action failed' });
    }
};

exports.getLikedDesigns = async (req, res) => {
    try {
        const user_id = req.user.id;
        const likedDesigns = await db('likes')
            .join('designs', 'likes.design_id', 'designs.design_id')
            .where('likes.user_id', user_id)
            .select('designs.*');

        res.json(likedDesigns);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch likes' });
    }
};

exports.getLikeStatus = async (req, res) => {
    try {
        const user_id = req.user.id;
        const { id: design_id } = req.params;
        const exists = await db('likes').where({ user_id, design_id }).first();
        res.json({ liked: !!exists });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch like status' });
    }
};
