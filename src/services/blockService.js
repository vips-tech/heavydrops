const db = require('../config/db');
const queueService = require('./queueService');

exports.createBlock = async (userId, designId, trx = null, referenceId = null) => {
    const execute = async (t) => {
        // 1. Verify User Constraints (Dynamic Limits)
        const user = await t('users').where({ user_id: userId }).first();
        const strikes = user ? (user.strike_count || 0) : 0;
        const maxActiveBlocks = strikes >= 2 ? 1 : (parseInt(process.env.ACTIVE_BLOCK_LIMIT) || 2);

        const activeBlocksCount = await t('blocks')
            .where({ user_id: userId, status: 'active' })
            .count('* as count')
            .first();

        if (activeBlocksCount.count >= maxActiveBlocks) {
            throw new Error(`Active block limit reached (${maxActiveBlocks}). Strike penalty active: ${strikes >= 2}`);
        }

        // 2. Verify Design Availability
        const design = await t('designs')
            .where({ design_id: designId, availability_status: 'available' })
            .first();

        if (!design) {
            throw new Error('Design is currently unavailable or already blocked.');
        }

        // 3. Verify Wallet Balance
        const wallet = await t('wallets').where({ user_id: userId }).first();
        const blockFee = parseInt(process.env.BLOCK_FEE_MIN); // For MVP, we use the static min fee

        if (!wallet || wallet.balance < blockFee) {
            throw new Error(`Insufficient wallet balance. Minimum block fee required: ₹${blockFee}`);
        }

        // 4. Calculate Expiry (T + 48h)
        const expiryTime = new Date();
        expiryTime.setHours(expiryTime.getHours() + parseInt(process.env.BLOCK_EXPIRY_HOURS));

        // 5. Execute Block Creation
        const designPrice = (design.weight * design.gold_rate_snapshot) + design.making_charge_snapshot;

        const [blockId] = await t('blocks').insert({
            user_id: userId,
            design_id: designId,
            price_snapshot: designPrice,
            status: 'active',
            expiry_time: expiryTime
        }, ['block_id']);

        // 6. Lock Design
        await t('designs')
            .where({ design_id: designId })
            .update({ availability_status: 'blocked' });

        // 7. Ledger Entry (Debit)
        await t('wallet_transactions').insert({
            wallet_id: wallet.wallet_id,
            amount: -blockFee,
            type: 'debit',
            source_type: 'block_payment',
            description: `Commitment fee for design #${designId}`,
            reference_id: referenceId // Added for security audit
        });

        // 8. Update Wallet Balance
        await t('wallets')
            .where({ user_id: userId })
            .update({
                balance: wallet.balance - blockFee,
                last_updated: t.fn.now()
            });

        // 9. Emit Notification Event
        await queueService.publish('block.created', {
            user_id: userId,
            design_id: designId,
            expiry_time: expiryTime
        }, t);

        return {
            block_id: blockId,
            expiry_time: expiryTime,
            locked_price: designPrice
        };
    };

    if (trx) {
        return await execute(trx);
    } else {
        return await db.transaction(execute);
    }
};

/**
 * Service to handle Block Expiry (Called by worker)
 */
exports.expireBlock = async (blockId) => {
    return await db.transaction(async (trx) => {
        const block = await trx('blocks').where({ block_id: blockId, status: 'active' }).first();
        if (!block) return;

        // 1. Release Design
        await trx('designs')
            .where({ design_id: block.design_id })
            .update({ availability_status: 'available' });

        // 2. Update Block Status
        await trx('blocks')
            .where({ block_id: blockId })
            .update({ status: 'expired' });

        // 3. Cancel Orphaned Appointments
        await trx('appointments')
            .where({ block_id: blockId, status: 'requested' })
            .update({ status: 'cancelled' });

        // 4. Emit Notification Event
        await queueService.publish('block.expired', {
            user_id: block.user_id,
            design_id: block.design_id
        }, trx);

        // Note: Intent Engine philosophy - Balance is NOT returned on expiry.
        // It remains in the system for platform decay or admin correction.
    });
};
