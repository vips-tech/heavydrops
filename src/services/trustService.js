const db = require('../config/db');
const queueService = require('./queueService');

/**
 * Penalize user for Showroom No-Show
 */
exports.penalizeNoShow = async (userId, blockId, trx = null) => {
    const execute = async (t) => {
        console.log(`[DEBUG] penalizeNoShow for User #${userId}, Block #${blockId}`);
        // 1. Add Strike
        const user = await t('users').where({ user_id: userId }).first();
        if (!user) {
            console.error(`[DEBUG] User #${userId} not found in trust penalty`);
            return;
        }

        const newStrikeCount = (user.strike_count || 0) + 1;

        await t('users').where({ user_id: userId }).update({
            strike_count: newStrikeCount,
            status: newStrikeCount >= 3 ? 'restricted' : 'active',
            updated_at: t.fn.now()
        });

        // 2. Financial Penalty (₹100 fine)
        const wallet = await t('wallets').where({ user_id: userId }).first();
        if (wallet && wallet.balance >= 100) {
            const penaltyRef = `PEN-${blockId}-${Date.now().toString().slice(-6)}`;
            await t('wallets').where({ user_id: userId }).decrement('balance', 100);
            await t('wallet_transactions').insert({
                wallet_id: wallet.wallet_id,
                amount: -100,
                type: 'debit',
                source_type: 'penalty',
                description: `No-show penalty for block #${blockId}`,
                reference_id: penaltyRef
            });
        }

        // 3. Log Violation
        await t('violations').insert({
            entity_type: 'user',
            entity_id: userId,
            type: 'no_show',
            level: newStrikeCount >= 3 ? 'high' : 'medium',
            reason: `Appointment no-show. Total strikes: ${newStrikeCount}`
        });

        // 4. Emit Notification
        await queueService.publish('appointment.no_show', {
            user_id: userId,
            block_id: blockId,
            strikes: newStrikeCount
        }, t);

        console.log(`[TRUST] No-show penalty applied to User #${userId}. Strikes: ${newStrikeCount}`);
    };

    if (trx) {
        return await execute(trx);
    } else {
        return await db.transaction(execute);
    }
};

/**
 * Update Seller Trust Score based on attendance/bypass
 */
exports.updateSellerTrust = async (sellerId, delta, reason) => {
    await db('sellers')
        .where({ seller_id: sellerId })
        .increment('trust_score', delta);

    await db('violations').insert({
        entity_type: 'seller',
        entity_id: sellerId,
        type: delta < 0 ? 'score_deduction' : 'score_increase',
        reason
    });
};
