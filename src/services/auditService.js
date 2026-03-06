const db = require('../config/db');

/**
 * Log a system action to the audit/violation logs
 */
exports.logAction = async ({ entityType, entityId, type, level = 'info', reason, userId = null }) => {
    try {
        await db('violations').insert({
            entity_type: entityType,
            entity_id: entityId,
            type: type,
            level: level,
            reason: reason,
            user_id_ref: userId, // Requires adding this field or using text
            created_at: db.fn.now()
        });

        console.log(`[AUDIT] ${type} logged for ${entityType} #${entityId}`);
    } catch (error) {
        console.error('[AUDIT] Failed to write log:', error.message);
    }
};

/**
 * Health Tracer (Observability)
 */
exports.traceHealth = async (action, success, category, userId = null) => {
    // Note: In MVP, we use console for high-frequency trace and DB for critical logs
    if (!success) {
        console.error(`[HEALTH_ALERT] ${category} failure during ${action} for User #${userId}`);
    }
};
