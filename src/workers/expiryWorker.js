const db = require('../config/db');
const blockService = require('../services/blockService');
const queueService = require('../services/queueService');

/**
 * The Block Expiry Worker
 * Scans for active blocks past their expiry_time and triggers release.
 */
const runExpiryJob = async () => {
    console.log('[WORKER] Starting Block Expiry scan...');
    try {
        const now = new Date();

        // Find up to 50 active blocks that have expired (Batching)
        const expiredBlocks = await db('blocks')
            .where('status', 'active')
            .where('expiry_time', '<=', now)
            .limit(50);

        // Find blocks nearing expiry (2 hours left)
        const warningTime = new Date(Date.now() + 2 * 60 * 60 * 1000);
        const nearingExpiry = await db('blocks')
            .where('status', 'active')
            .where('expiry_time', '<=', warningTime)
            .where('expiry_time', '>', now);

        for (const block of nearingExpiry) {
            await queueService.publish('block.expiry_warning', {
                user_id: block.user_id,
                design_id: block.design_id
            });
        }

        console.log(`[WORKER] Found ${expiredBlocks.length} blocks to expire.`);

        for (const block of expiredBlocks) {
            await blockService.expireBlock(block.block_id);
            console.log(`[WORKER] Expired Block #${block.block_id} (Design #${block.design_id})`);
        }

        if (expiredBlocks.length > 0) {
            console.log(`[WORKER] Successfully flushed ${expiredBlocks.length} design blocks.`);
        }
    } catch (error) {
        console.error('[WORKER] Block expiry job failed:', error);
    }
};

/**
 * Audit Wallets for Long Inactivity (Simulated Expiry)
 */
const auditWalletActivity = async () => {
    console.log('[WORKER] Starting Wallet Activity Audit...');
    try {
        // Mock audit: Update last_updated or flag inactive wallets
        // In this platform, intent doesn't die, it just needs reconciliation.
        const staleWallets = await db('wallets')
            .where('last_updated', '<', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)); // 30 days

        console.log(`[WORKER] Audited ${staleWallets.length} inactive wallets.`);
    } catch (error) {
        console.error('[WORKER] Wallet audit failed:', error);
    }
};

/**
 * Handle Appointment Reminders
 */
const processAppointmentReminders = async () => {
    console.log('[WORKER] Checking for upcoming appointment reminders...');
    try {
        const soon = new Date(Date.now() + 2 * 60 * 60 * 1000); // 2 hours from now
        const reminders = await db('appointments')
            .where('status', 'confirmed')
            .where('appointment_time', '<=', soon);

        for (const appt of reminders) {
            console.log(`[WORKER] [REMINDER] Alerting User #${appt.user_id} for appointment #${appt.appointment_id}`);
            await queueService.publish('appointment.reminder', {
                user_id: appt.user_id,
                design_id: appt.design_id,
                time: appt.appointment_time
            });
        }
    } catch (error) {
        console.error('[WORKER] Reminder job failed:', error);
    }
};

/**
 * Abuse Detection: Flag accounts with high strikes
 */
const processAbuseDetection = async () => {
    console.log('[WORKER] Scanning for platform abuse signals...');
    try {
        // Find users with strike_count >= 3 who are not yet suspended
        const suspiciousUsers = await db('users')
            .where('strike_count', '>=', 3)
            .where('role', '!=', 'suspended');

        for (const user of suspiciousUsers) {
            console.log(`[WORKER] [ABUSE] Automated suspension for User #${user.user_id} due to strike count (${user.strike_count})`);

            await db.transaction(async trx => {
                // 1. Suspend User
                await trx('users').where({ user_id: user.user_id }).update({
                    role: 'suspended',
                    updated_at: trx.fn.now()
                });

                // 2. Log Violation
                await trx('violations').insert({
                    entity_type: 'buyer',
                    entity_id: user.user_id,
                    type: 'abuse_automated',
                    reason: 'Automated suspension: Strike count limit (3) exceeded.',
                    level: 'critical'
                });

                // 3. (Optional) Flush all active blocks
                const activeBlocks = await trx('blocks').where({ user_id: user.user_id, status: 'active' });
                for (const block of activeBlocks) {
                    await blockService.expireBlock(block.block_id);
                }
            });
        }
    } catch (error) {
        console.error('[WORKER] Abuse detection failed:', error);
    }
};

// Simple polling mechanism for MVP (10-minute interval)
const startWorker = () => {
    console.log('[SYSTEM] Background Worker Initialized.');
    // Expiry: Every 10 minutes
    setInterval(runExpiryJob, 10 * 60 * 1000);
    // Wallets: Every 24 hours
    setInterval(auditWalletActivity, 24 * 60 * 60 * 1000);
    // Reminders: Every 15 minutes
    setInterval(processAppointmentReminders, 15 * 60 * 1000);
    // Abuse: Every 6 hours
    setInterval(processAbuseDetection, 6 * 60 * 60 * 1000);

    // Initial run on startup
    runExpiryJob();
    auditWalletActivity();
    processAppointmentReminders();
    processAbuseDetection();
};

module.exports = { startWorker };
