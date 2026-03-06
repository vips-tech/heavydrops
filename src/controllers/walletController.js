const db = require('../config/db');

/**
 * Get Wallet Information
 */
exports.getWalletInfo = async (req, res) => {
    try {
        const userId = req.user.id;

        // Fetch Wallet & User details
        const [wallet, user] = await Promise.all([
            db('wallets').where({ user_id: userId }).first(),
            db('users').where({ user_id: userId }).first()
        ]);

        if (!wallet) return res.status(404).json({ error: 'Wallet not found' });

        // Count Active Blocks
        const activeBlocks = await db('blocks')
            .where({ user_id: userId, status: 'active' })
            .count('* as count')
            .first();

        res.json({
            balance: wallet.balance,
            expiry_date: wallet.expiry_date,
            is_expired: wallet.expiry_date ? (new Date(wallet.expiry_date) < new Date()) : false,
            active_blocks_count: parseInt(activeBlocks.count),
            strike_count: user.strike_count || 0,
            status: user.status === 'active' ? 'Good Standing' : 'Restricted',
            is_verified: true // Based on OTP-driven login model
        });
    } catch (error) {
        console.error('[WALLET] Error fetching info:', error);
        res.status(500).json({ error: 'Failed to fetch wallet info' });
    }
};

/**
 * Get Full Transaction Ledger
 */
exports.getLedger = async (req, res) => {
    try {
        const userId = req.user.id;
        const wallet = await db('wallets').where({ user_id: userId }).first();
        if (!wallet) return res.status(404).json({ error: 'Wallet not found' });

        const transactions = await db('wallet_transactions')
            .where({ wallet_id: wallet.wallet_id })
            .orderBy('created_at', 'desc');

        res.json(transactions);
    } catch (error) {
        console.error('[WALLET] Error fetching ledger:', error);
        res.status(500).json({ error: 'Failed to fetch transaction ledger' });
    }
};
