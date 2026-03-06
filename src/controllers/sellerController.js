const db = require('../config/db');
const { z } = require('zod');
const path = require('path');

/**
 * Get Seller Profile & Performance
 */
exports.getSellerProfile = async (req, res) => {
    try {
        const { sellerId } = req.params;
        const seller = await db('sellers').where({ seller_id: sellerId }).first();
        if (!seller) return res.status(404).json({ error: 'Seller not found' });

        const designs = await db('designs').where({ seller_id: sellerId, availability_status: 'available' });

        res.json({
            ...seller,
            collection: designs
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch seller profile' });
    }
};

/**
 * Get Seller Dashboard Data (Blocks & Appointments)
 */
exports.getDashboardData = async (req, res) => {
    try {
        const sellerId = req.params.sellerId; // In real app, derived from req.user

        const activeBlocks = await db('blocks')
            .join('designs', 'blocks.design_id', 'designs.design_id')
            .where('designs.seller_id', sellerId)
            .where('blocks.status', 'active')
            .select('blocks.*', 'designs.category', 'designs.purity');

        const appointments = await db('appointments')
            .join('users', 'appointments.user_id', 'users.user_id')
            .where('appointments.seller_id', sellerId)
            .select('appointments.*', 'users.phone');

        // Aggregate Metrics Calculation
        const designStats = await db('designs')
            .where({ seller_id: sellerId })
            .select(
                db.raw('SUM(view_count) as total_views'),
                db.raw('COUNT(designs.design_id) as total_designs')
            )
            .first();

        const totalLikes = await db('likes')
            .join('designs', 'likes.design_id', 'designs.design_id')
            .where('designs.seller_id', sellerId)
            .count('* as count')
            .first();

        // Anonymize numbers for privacy
        const anonymizedAppts = appointments.map(a => ({
            ...a,
            phone: '******' + a.phone.slice(-4)
        }));

        res.json({
            metrics: {
                total_views: parseInt(designStats.total_views) || 0,
                total_likes: parseInt(totalLikes.count) || 0,
                total_active_intent: activeBlocks.length,
                pending_appointments: appointments.filter(a => a.status === 'requested').length
            },
            blocks: activeBlocks,
            appointments: anonymizedAppts
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch dashboard data' });
    }
};

/**
 * Get Authenticated User's Seller Profile
 */
exports.getMySellerProfile = async (req, res) => {
    try {
        const userId = req.user.id;
        const seller = await db('sellers').where({ user_id: userId }).first();

        if (!seller) {
            return res.status(404).json({ error: 'No seller profile associated with this account.' });
        }

        res.json(seller);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch your seller profile' });
    }
};

/**
 * Mark Appointment Outcome (Attended / No-show)
 */
exports.markAppointmentOutcome = async (req, res) => {
    const schema = z.object({
        outcome: z.enum(['attended', 'no-show'])
    });

    try {
        const { appointment_id } = req.params;
        const { outcome } = schema.parse(req.body);
        const trustService = require('../services/trustService');

        const appt = await db('appointments').where({ appointment_id }).first();
        if (!appt) {
            return res.status(404).json({ error: 'Appointment not found' });
        }

        await db.transaction(async (trx) => {
            await trx('appointments').where({ appointment_id }).update({
                status: outcome === 'attended' ? 'attended' : 'no_show',
                seller_notes: outcome
            });

            if (outcome === 'attended') {
                await trx('blocks')
                    .where({ block_id: appt.block_id })
                    .update({ status: 'converted' });

                await trx('designs')
                    .where({ design_id: appt.design_id })
                    .update({ availability_status: 'sold' });
            }

            if (outcome === 'no-show') {
                await trustService.penalizeNoShow(appt.user_id, appt.block_id, trx);
            }
        });

        res.json({ message: `Outcome marked as ${outcome}` });
    } catch (error) {
        res.status(500).json({ error: 'Failed to mark outcome: ' + error.message });
    }
};

exports.getDesignPerformance = async (req, res) => {
    try {
        const { sellerId } = req.params;

        const designs = await db('designs')
            .where({ seller_id: sellerId })
            .select('design_id', 'category', 'purity', 'view_count', 'availability_status');

        const performanceData = await Promise.all(designs.map(async (d) => {
            const likesCount = await db('likes').where({ design_id: d.design_id }).count('* as count').first();
            const blocksCount = await db('blocks').where({ design_id: d.design_id }).count('* as count').first();

            return {
                ...d,
                likes: parseInt(likesCount.count) || 0,
                blocks: parseInt(blocksCount.count) || 0
            };
        }));

        res.json(performanceData);
    } catch (error) {
        console.error('[SELLER] Performance fetch failed:', error);
        res.status(500).json({ error: 'Failed to fetch performance data' });
    }
};

exports.updateDesign = async (req, res) => {
    try {
        const { designId } = req.params;
        const updates = req.body;

        const design = await db('designs').where({ design_id: designId }).first();
        if (!design) return res.status(404).json({ error: 'Design not found' });

        // Rule Enforcement: No price changes after block
        if (design.availability_status === 'blocked' && (updates.gold_rate_snapshot || updates.making_charge_snapshot)) {
            return res.status(403).json({ error: 'SELLER SYSTEM BREACH: Price modification forbidden during active intent block.' });
        }

        await db('designs').where({ design_id: designId }).update(updates);
        res.json({ message: 'Design updated successfully' });
    } catch (error) {
        res.status(500).json({ error: 'Update failed' });
    }
};

/**
 * Controlled Photography Upload
 * Enforces ownership and media standards
 */
exports.uploadDesignMedia = async (req, res) => {
    try {
        const { designId } = req.params;
        const { shot_type } = req.body; // master, closeup, worn
        const userId = req.user.id;

        // 1. Ownership & Authority Bridge (CRITICAL)
        const design = await db('designs')
            .where({ design_id: designId })
            .join('sellers', 'designs.seller_id', 'sellers.seller_id')
            .select('designs.*', 'sellers.user_id')
            .first();

        if (!design) {
            return res.status(404).json({ error: 'Design not found' });
        }

        if (design.user_id !== userId) {
            console.error(`[SECURITY] Cross-seller upload attempt detected. User #${userId} tried to upload to Design #${designId}`);
            return res.status(403).json({ error: 'Unauthorized: You do not own this design' });
        }

        // 2. Validate Files
        if (!req.files || req.files.length === 0) {
            return res.status(400).json({ error: 'No files uploaded' });
        }

        // 3. Persistent DB Linking
        const mediaEntries = req.files.map(file => ({
            design_id: designId,
            uri: `/uploads/designs/${file.filename}`,
            media_type: 'image',
            shot_type: shot_type || 'master',
            status: 'pending_review'
        }));

        await db.transaction(async trx => {
            await trx('design_media').insert(mediaEntries);

            // Mark design for re-audit if it was already approved/rejected
            await trx('designs').where({ design_id: designId }).update({
                media_quality_status: 'pending',
                updated_at: trx.fn.now()
            });
        });

        res.status(201).json({
            message: 'Photography uploaded and pending review.',
            count: mediaEntries.length
        });
    } catch (error) {
        console.error('[PHOTOGRAPHY] Upload failed:', error);
        res.status(500).json({ error: 'Upload infrastructure failure' });
    }
};
