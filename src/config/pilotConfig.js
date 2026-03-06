/**
 * Jewellery Discovery & Intent Platform: Pilot Configuration
 */

module.exports = {
    // System Mode: PILOT or SCALE
    PILOT_MODE: process.env.PILOT_MODE === 'true' || true, // Default to true for MVP

    // Pilot Constraints
    PILOT_CONSTRAINTS: {
        MAX_SELLERS: 25,
        MAX_BUYERS: 1000,
        RESTRICTED_CITY: 'Mumbai',
        ALLOW_SELF_ONBOARDING: false
    },

    // Feature Flags - Admin Controlled
    FEATURES: {
        AI_TRY_ON: false,
        ONLINE_PURCHASE: false, // Core Hard Constraint: NO ECOMMERCE
        CUSTOM_FLOW: false,
        SELLER_INSIGHTS: false,
        BOOST_LISTINGS: false
    },

    /**
     * Helper to check if a feature is enabled
     */
    isFeatureEnabled: (featureName) => {
        return !!module.exports.FEATURES[featureName];
    }
};
