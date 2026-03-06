const db = require('../config/db');

/**
 * Notification Rate Limiter
 * Ensures max 5 SMS per hour per user.
 */
class RateLimiter {
    async canSendSMS(userId) {
        const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
        const count = await db('notifications')
            .where({ user_id: userId, channel: 'sms' })
            .where('created_at', '>=', oneHourAgo)
            .count('* as count')
            .first();

        return parseInt(count.count) < 5;
    }
}

module.exports = new RateLimiter();
