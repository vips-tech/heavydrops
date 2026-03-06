const db = require('../config/db');

/**
 * Get System Health & Telemetry
 */
exports.getSystemHealth = async (req, res) => {
    try {
        // 1. Active Intent Metrics
        const activeBlocks = await db('blocks').where('status', 'active').count('* as count').first();
        const convertedBlocks = await db('blocks').where('status', 'converted').count('* as count').first();

        // 2. Financial Integrity (Wallet Reconcile)
        const walletTotal = await db('wallets').sum('balance as total').first();

        // 3. User Reputation Stats
        const totalStrikes = await db('users').sum('strike_count as total').first();

        // 4. Listing Curation Stats
        const pendingListings = await db('designs').where('media_quality_status', 'pending').count('* as count').first();

        res.json({
            status: 'healthy',
            timestamp: new Date(),
            metrics: {
                active_blocks: parseInt(activeBlocks.count),
                conversion_count: parseInt(convertedBlocks.count),
                total_platform_wallet: parseFloat(walletTotal.total || 0),
                curation_backlog: parseInt(pendingListings.count),
                abuse_signals: {
                    total_strikes: parseInt(totalStrikes.total || 0)
                }
            }
        });
    } catch (error) {
        console.error('[HEALTH] Telemetry failed:', error);
        res.status(500).json({ error: 'Failed to retrieve system health' });
    }
};

/**
 * Get public system configuration & feature flags
 */
exports.getSystemConfig = (req, res) => {
    const config = require('../config/pilotConfig');
    res.json({
        pilot_mode: config.PILOT_MODE,
        features: config.FEATURES,
        constraints: config.PILOT_MODE ? config.PILOT_CONSTRAINTS : null
    });
};
