const db = require('../config/db');
const messagingService = require('../services/messagingService');
const rateLimiter = require('../services/rateLimiter');

/**
 * Notification Worker
 * Consumes events from the database queue and dispatches calm, branded notifications.
 */
class NotificationWorker {
    constructor() {
        this.isRunning = false;
        this.templates = {
            'block.created': (p) => `Block Confirmation: Design #${p.design_id} is now reserved for you. Expiring in 48 hours.`,
            'block.expiry_warning': (p) => `Nearing Expiry: Your block for Design #${p.design_id} expires in 2 hours.`,
            'block.expired': (p) => `Block Expired: Design #${p.design_id} has been released back to the collection.`,
            'appointment.booked': (p) => `Showroom Visit: Your appointment for Design #${p.design_id} is scheduled for ${p.time}.`,
            'appointment.reminder': (p) => `Reminder: You have a showroom visit scheduled for today at ${p.time}.`,
            'appointment.no_show': (p) => `Missed Visit: A no-show was logged for your visit. Your trust score has been adjusted.`,
            'seller.violation': (p) => `Governance Notice: A violation (${p.type}) has been logged. Please review platform guidelines.`
        };
    }

    async start() {
        if (this.isRunning) return;
        this.isRunning = true;
        console.log('[NOTIFIER] Notification Worker Active.');

        // Loop every 30 seconds for MVP
        setInterval(() => this.processQueue(), 30000);
    }

    async processQueue() {
        try {
            const jobs = await db('notification_queue')
                .where('status', 'pending')
                .orWhere(function () {
                    this.where('status', 'failed').andWhere('attempts', '<', 3);
                })
                .where('next_attempt_at', '<=', db.fn.now())
                .limit(10);

            for (const job of jobs) {
                await this.processJob(job);
            }
        } catch (error) {
            console.error('[NOTIFIER] Queue processing error:', error.message);
        }
    }

    async processJob(job) {
        const payload = JSON.parse(job.payload);
        const userId = payload.user_id;
        const message = this.templates[job.event_type] ? this.templates[job.event_type](payload) : 'Platform Update';

        try {
            await db('notification_queue').where({ job_id: job.job_id }).update({ status: 'processing' });

            const channel = this.getPriorityChannel(job.event_type);
            let dispatchSuccess = false;

            if (channel === 'sms') {
                if (await rateLimiter.canSendSMS(userId)) {
                    dispatchSuccess = await messagingService.sendSMS(userId, message);
                } else {
                    console.warn(`[NOTIFIER] SMS Rate limit hit for User #${userId}. Falling back to Email...`);
                    dispatchSuccess = await messagingService.sendEmail(userId, message);
                }
            } else if (channel === 'email') {
                dispatchSuccess = await messagingService.sendEmail(userId, message);
            } else {
                dispatchSuccess = await messagingService.sendInApp(userId, message);
            }

            if (dispatchSuccess) {
                await db('notifications').insert({
                    user_id: userId,
                    type: job.event_type,
                    channel: channel,
                    status: 'sent',
                    payload: job.payload
                });
                await db('notification_queue').where({ job_id: job.job_id }).update({ status: 'completed' });
            }
        } catch (error) {
            console.error(`[NOTIFIER] Job #${job.job_id} failed:`, error.message);
            await db('notification_queue').where({ job_id: job.job_id }).update({
                status: 'failed',
                attempts: job.attempts + 1,
                next_attempt_at: new Date(Date.now() + 5 * 60 * 1000)
            });
        }
    }

    getPriorityChannel(type) {
        if (['block.created', 'appointment.booked', 'appointment.no_show'].includes(type)) return 'sms';
        if (['block.expiry_warning', 'appointment.reminder', 'seller.violation'].includes(type)) return 'email';
        return 'in_app';
    }
}

module.exports = new NotificationWorker();
