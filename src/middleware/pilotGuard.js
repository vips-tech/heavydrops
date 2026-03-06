const config = require('../config/pilotConfig');
const db = require('../config/db');

/**
 * Pilot Guard Middleware
 */
module.exports = {
    /**
     * Enforce Seller Cap
     */
    sellerCapGuard: async (req, res, next) => {
        if (!config.PILOT_MODE) return next();

        const sellerCount = await db('sellers').count('seller_id as count').first();
        if (sellerCount.count >= config.PILOT_CONSTRAINTS.MAX_SELLERS) {
            return res.status(403).json({
                error: 'Pilot Limit Reached',
                message: `The platform is currently limited to ${config.PILOT_CONSTRAINTS.MAX_SELLERS} curated sellers during the pilot phase.`
            });
        }
        next();
    },

    /**
     * Enforce Geographic Lock
     */
    geoLockGuard: (req, res, next) => {
        if (!config.PILOT_MODE) return next();

        const { city } = req.body;
        if (city && city !== config.PILOT_CONSTRAINTS.RESTRICTED_CITY) {
            return res.status(403).json({
                error: 'Restricted Geography',
                message: `During pilot, discovery is limited to ${config.PILOT_CONSTRAINTS.RESTRICTED_CITY}.`
            });
        }
        next();
    },

    /**
     * Prevent Self-Onboarding in Pilot
     */
    onboardingGuard: (req, res, next) => {
        if (config.PILOT_MODE && !config.PILOT_CONSTRAINTS.ALLOW_SELF_ONBOARDING) {
            return res.status(403).json({
                error: 'Invite Required',
                message: 'Self-onboarding is disabled during pilot. Please contact platform admin.'
            });
        }
        next();
    }
};
