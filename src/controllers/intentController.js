const db = require('../config/db');
const blockService = require('../services/blockService');
const z = require('zod');

/**
 * Handle Intent Block Creation
 */
exports.createIntentBlock = async (req, res) => {
    const schema = z.object({
        design_id: z.number()
    });

    try {
        const { design_id } = schema.parse(req.body);
        const user_id = req.user.id;

        const result = await blockService.createBlock(user_id, design_id);

        res.status(201).json({
            message: 'Design blocked successfully',
            data: result
        });
    } catch (error) {
        console.error('[INTENT] Block failed:', error.message);
        res.status(400).json({ error: error.message });
    }
};

exports.getWallet = async (req, res) => {
    try {
        const { userId } = req.params;

        const wallet = await db('wallets')
            .where({ user_id: userId })
            .first();

        if (!wallet) return res.status(404).json({ error: 'Wallet not found' });

        const transactions = await db('wallet_transactions')
            .where({ wallet_id: wallet.wallet_id })
            .orderBy('created_at', 'desc')
            .limit(10);

        res.json({
            balance: wallet.balance,
            last_updated: wallet.last_updated,
            recent_activity: transactions
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch wallet info' });
    }
};

exports.getLedger = async (req, res) => {
    try {
        const { userId } = req.params;
        const wallet = await db('wallets').where({ user_id: userId }).first();
        if (!wallet) return res.status(404).json({ error: 'Wallet not found' });

        const transactions = await db('wallet_transactions')
            .where({ wallet_id: wallet.wallet_id })
            .orderBy('created_at', 'desc');

        res.json(transactions);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch ledger' });
    }
};

exports.getBlockStatus = async (req, res) => {
    try {
        const { designId } = req.params;
        const user_id = req.user.id;

        const block = await db('blocks')
            .where({ design_id: designId, status: 'active' })
            .first();

        if (!block) {
            return res.json({ status: 'available' });
        }

        if (block.user_id === user_id) {
            return res.json({
                status: 'blocked_by_me',
                expiry_time: block.expiry_time
            });
        }

        res.json({ status: 'blocked_by_other' });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch block status' });
    }
};
