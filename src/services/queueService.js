const db = require('../config/db');

/**
 * Internal Queue Service for Event Publishing
 * This implements a database-backed queue for the MVP Operational Layer.
 */
class QueueService {
    /**
     * Publish an event to the notification queue
     * @param {string} event - The event type (e.g., 'block.created')
     * @param {object} payload - The event data
     * @param {object} trx - Optional transaction object
     */
    async publish(event, payload, trx = null) {
        const t = trx || db;
        try {
            await t('notification_queue').insert({
                event_type: event,
                payload: JSON.stringify(payload),
                status: 'pending',
                next_attempt_at: db.fn.now()
            });
            console.log(`[QUEUE] Event Published: ${event}`);
        } catch (error) {
            console.error(`[QUEUE] Failed to publish event ${event}:`, error.message);
        }
    }
}

module.exports = new QueueService();
