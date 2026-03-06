const db = require('../config/db');
const queueService = require('../services/queueService');
const { z } = require('zod');

/**
 * Admin Audit Logger
 */
async function logAdminAction(adminId, action, targetEntity, targetId, description, trx = null) {
    const t = trx || db;
    await t('admin_logs').insert({
        admin_id: adminId,
        action,
        target_entity: targetEntity,
        target_id: targetId,
        description
    });
}

/**
 * Get Master Platform Overview
 */
exports.getStats = async (req, res) => {
    try {
        const userCount = await db('users').count('* as count').first();
        const sellerCount = await db('sellers').count('* as count').first();
        const activeBlocks = await db('blocks').where('status', 'active').count('* as count').first();
        const totalWallet = await db('wallets').sum('balance as total').first();

        res.json({
            users: parseInt(userCount.count),
            sellers: parseInt(sellerCount.count),
            active_intent_blocks: parseInt(activeBlocks.count),
            platform_wallet_balance: parseFloat(totalWallet.total || 0)
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch admin stats' });
    }
};

/**
 * Manage Sellers (Approval/Suspension)
 */
exports.updateSellerStatus = async (req, res) => {
    const schema = z.object({
        status: z.enum(['active', 'suspended', 'applicant'])
    });

    try {
        const { seller_id } = req.params;
        const { status } = schema.parse(req.body);

        await db.transaction(async trx => {
            await trx('sellers').where({ seller_id }).update({ membership_status: status });
            await logAdminAction(req.user.id, 'update_seller_status', 'seller', seller_id, `Status set to ${status}`, trx);
        });

        res.json({ message: `Seller status updated to ${status}` });
    } catch (error) {
        res.status(400).json({ error: error.errors || error.message });
    }
};

/**
 * Adjust User Wallet (Platform Credit/Correction)
 */
exports.adjustWallet = async (req, res) => {
    const schema = z.object({
        user_id: z.number(),
        amount: z.number(),
        reason: z.string().min(5)
    });

    try {
        const { user_id, amount, reason } = schema.parse(req.body);
        const cycleRef = 'ADM-' + Math.random().toString(36).substr(2, 9).toUpperCase();

        await db.transaction(async trx => {
            const wallet = await trx('wallets').where({ user_id }).first();
            if (!wallet) throw new Error('Wallet not found');

            const newBalance = wallet.balance + amount;
            await trx('wallets').where({ user_id }).update({ balance: newBalance });

            await trx('wallet_transactions').insert({
                wallet_id: wallet.wallet_id,
                amount: amount,
                type: amount > 0 ? 'credit' : 'debit',
                source_type: 'correction',
                description: reason,
                reference_id: cycleRef
            });

            await logAdminAction(req.user.id, 'adjust_wallet', 'user', user_id, `Adjusted by ${amount}. Reason: ${reason}. Ref: ${cycleRef}`, trx);
        });

        res.json({ message: 'Wallet adjusted successfully' });
    } catch (error) {
        res.status(400).json({ error: error.errors || error.message });
    }
};

/**
 * View All Active Blocks
 */
exports.getAllBlocks = async (req, res) => {
    try {
        const blocks = await db('blocks')
            .join('users', 'blocks.user_id', 'users.user_id')
            .join('designs', 'blocks.design_id', 'designs.design_id')
            .select('blocks.*', 'users.phone', 'designs.category');
        res.json(blocks);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch all blocks' });
    }
};

/**
 * Fetch All Sellers for Platform Governance
 */
exports.getSellers = async (req, res) => {
    try {
        const { status } = req.query;
        let query = db('sellers');
        if (status) query = query.where({ membership_status: status });

        const sellers = await query.select('*');
        res.json(sellers);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch sellers' });
    }
};

/**
 * Approve/Reject Designs (Visual Photography Audit)
 */
exports.approveListing = async (req, res) => {
    const schema = z.object({
        status: z.enum(['approved', 'rejected'])
    });

    try {
        const { design_id } = req.params;
        const { status } = schema.parse(req.body);

        await db.transaction(async trx => {
            await trx('designs').where({ design_id }).update({
                media_quality_status: status,
                availability_status: status === 'approved' ? 'available' : 'rejected'
            });
            await logAdminAction(req.user.id, 'approve_listing', 'design', design_id, `Photography audit: ${status}`, trx);
        });

        res.json({ message: `Photography Audit: Listing ${status}` });
    } catch (error) {
        res.status(400).json({ error: error.errors || error.message });
    }
};

/**
 * Get Designs Pending Audit
 */
exports.getPendingDesigns = async (req, res) => {
    try {
        const designs = await db('designs')
            .join('sellers', 'designs.seller_id', 'sellers.seller_id')
            .leftJoin('design_media', 'designs.design_id', 'design_media.design_id')
            .where('designs.media_quality_status', 'pending')
            .orWhere('design_media.status', 'pending_review')
            .select('designs.*', 'sellers.business_name')
            .distinct();
        res.json(designs);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch pending designs' });
    }
};

/**
 * Platform User Management
 */
exports.getUsers = async (req, res) => {
    try {
        const users = await db('users')
            .leftJoin('wallets', 'users.user_id', 'wallets.user_id')
            .select('users.*', 'wallets.balance');
        res.json(users);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch users' });
    }
};

exports.updateUserStatus = async (req, res) => {
    const schema = z.object({
        status: z.enum(['active', 'restricted', 'suspended'])
    });

    try {
        const { user_id } = req.params;
        const { status } = schema.parse(req.body);

        await db.transaction(async trx => {
            await trx('users').where({ user_id }).update({
                role: status === 'suspended' ? 'visitor' : (status === 'active' ? 'buyer' : 'restricted'),
                updated_at: db.fn.now()
            });
            await logAdminAction(req.user.id, 'update_user_status', 'user', user_id, `Status set to ${status}`, trx);
        });

        res.json({ message: `User status updated to ${status}` });
    } catch (error) {
        res.status(400).json({ error: error.errors || error.message });
    }
};

/**
 * Violation & Governance Desk
 */
exports.logViolation = async (req, res) => {
    try {
        const { entity_type, entity_id, type, reason, level } = req.body;

        await db.transaction(async trx => {
            await trx('violations').insert({
                entity_type,
                entity_id,
                type,
                reason,
                level: level || 'warning'
            });

            if (entity_type === 'buyer' && level === 'strike') {
                await trx('users').where({ user_id: entity_id }).increment('strike_count', 1);
            }

            // Emit Notification for Seller Violation
            if (entity_type === 'seller') {
                await queueService.publish('seller.violation', {
                    user_id: entity_id,
                    type: type,
                    reason: reason
                }, trx);
            }
        });

        res.status(201).json({ message: 'Violation recorded successfully' });
    } catch (error) {
        res.status(500).json({ error: 'Failed to log violation' });
    }
};

/**
 * Operational Monitoring (Consolidated View)
 */
exports.getAppointmentsSummary = async (req, res) => {
    try {
        const appointments = await db('appointments')
            .join('users', 'appointments.user_id', 'users.user_id')
            .join('sellers', 'appointments.seller_id', 'sellers.seller_id')
            .join('blocks', 'appointments.block_id', 'blocks.block_id')
            .select(
                'appointments.*',
                'users.phone as buyer_phone',
                'sellers.business_name as seller_brand',
                'blocks.status as block_current_status'
            )
            .orderBy('appointment_time', 'desc');

        res.json(appointments);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch appointment patterns' });
    }
};

exports.getViolations = async (req, res) => {
    try {
        const violations = await db('violations').orderBy('created_at', 'desc');
        res.json(violations);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch violation history' });
    }
};

/**
 * Review Design Media (Quality Control Gate)
 */
exports.reviewDesignMedia = async (req, res) => {
    const schema = z.object({
        status: z.enum(['approved', 'rejected']),
        reason: z.string().optional()
    });

    try {
        const { media_id } = req.params;
        const { status, reason } = schema.parse(req.body);

        await db.transaction(async trx => {
            const media = await trx('design_media').where({ media_id }).first();
            if (!media) throw new Error('Media entry not found');

            // 1. Update Media Status
            await trx('design_media').where({ media_id }).update({
                status,
                updated_at: trx.fn.now()
            });

            // 2. Audit Trail
            await logAdminAction(req.user.id, 'review_media', 'design_media', media_id, `Photography review: ${status}. ${reason || ''}`, trx);

            // 3. Logic Bridge: If master shot is approved, check if design can be available
            if (status === 'approved' && media.shot_type === 'master') {
                await trx('designs').where({ design_id: media.design_id }).update({
                    media_quality_status: 'approved',
                    availability_status: 'available'
                });
            }

            // If all media for a design are rejected, mark design as rejected
            if (status === 'rejected') {
                const remainingApproved = await trx('design_media')
                    .where({ design_id: media.design_id, status: 'approved' })
                    .count('* as count')
                    .first();

                if (parseInt(remainingApproved.count) === 0) {
                    await trx('designs').where({ design_id: media.design_id }).update({
                        media_quality_status: 'rejected',
                        availability_status: 'rejected'
                    });
                }
            }
        });

        res.json({ message: `Media review: ${status}` });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};

exports.getPendingMedia = async (req, res) => {
    try {
        const pendingMedia = await db('design_media')
            .join('designs', 'design_media.design_id', 'designs.design_id')
            .join('sellers', 'designs.seller_id', 'sellers.seller_id')
            .where('design_media.status', 'pending_review')
            .select('design_media.*', 'sellers.business_name', 'designs.category');

        res.json(pendingMedia);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch pending media' });
    }
};

/**
 * Gold Rate Management
 */
exports.getGoldRate = async (req, res) => {
    try {
        const rates = await db('gold_rates')
            .whereIn('purity', ['22K', '24K'])
            .orderBy('updated_at', 'desc');

        // Return latest rate for each purity
        const latest = rates.reduce((acc, r) => {
            if (!acc[r.purity]) acc[r.purity] = r;
            return acc;
        }, {});

        res.json(latest);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch gold rates' });
    }
};

exports.updateGoldRate = async (req, res) => {
    const schema = z.object({
        purity: z.enum(['22K', '24K']),
        rate: z.number().positive()
    });

    try {
        const { purity, rate } = schema.parse(req.body);

        await db.transaction(async trx => {
            await trx('gold_rates').insert({
                purity,
                rate_per_gram: rate,
                updated_at: trx.fn.now()
            });
            await logAdminAction(req.user.id, 'update_gold_rate', 'gold_rates', purity, `Updated ${purity} rate to ₹${rate}`, trx);
        });

        res.json({ message: `Gold rate for ${purity} updated to ₹${rate}` });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};
