const db = require('../config/db');

/**
 * Verify wallet-ledger consistency for all users
 */
exports.verifyAllWallets = async () => {
    console.log('[INTEGRITY] Verifying wallet-ledger consistency...');

    const wallets = await db('wallets').select('*');
    const discrepancies = [];

    for (const wallet of wallets) {
        const txSum = await db('wallet_transactions')
            .where({ wallet_id: wallet.wallet_id })
            .sum('amount as total');

        const calculatedBalance = parseFloat(txSum[0].total || 0);
        const currentBalance = parseFloat(wallet.balance);

        if (calculatedBalance !== currentBalance) {
            console.error(`[INTEGRITY] Discrepancy detected for Wallet #${wallet.wallet_id}: Calculated=${calculatedBalance}, Actual=${currentBalance}`);
            discrepancies.push({
                wallet_id: wallet.wallet_id,
                user_id: wallet.user_id,
                calculated: calculatedBalance,
                actual: currentBalance
            });
        }
    }

    if (discrepancies.length === 0) {
        console.log('[INTEGRITY] Verification complete: All wallets are consistent.');
        return { success: true, count: wallets.length };
    } else {
        console.error(`[INTEGRITY] Found ${discrepancies.length} inconsistencies.`);
        return { success: false, discrepancies };
    }
};
