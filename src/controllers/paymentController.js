const db = require('../config/db');
const blockService = require('../services/blockService');

/**
 * Initiate a Payment for a Design Block
 */
exports.initiatePayment = async (req, res) => {
    try {
        const { design_id } = req.body;
        const user_id = req.user.id;

        // Verify if user already has 2 active blocks
        const activeBlocks = await db('blocks').where({ user_id, status: 'active' }).count('* as count').first();
        if (activeBlocks.count >= 2) {
            return res.status(400).json({ error: 'Max 2 active intent blocks allowed.' });
        }

        // Generate mock transaction ID
        const transactionId = 'TXN-' + Math.random().toString(36).substr(2, 9).toUpperCase();
        const blockFee = parseInt(process.env.BLOCK_FEE_MIN) || 500;

        // In a real app, this would return a gateway URL. 
        // For MVP, we return a success token to simulate callback.
        res.json({
            message: 'Payment initiated',
            transaction_id: transactionId,
            block_fee: blockFee,
            gateway_sim_url: `/pay-sim.html?design_id=${design_id}`
        });
    } catch (error) {
        res.status(500).json({ error: 'Payment initiation failed' });
    }
};

/**
 * Mock Gateway Callback (Web-Hook)
 */
exports.handleSuccess = async (req, res) => {
    console.log('[DEBUG] Entering handleSuccess');
    try {
        const { design_id, status } = req.body;
        const user_id = req.user.id;
        console.log(`[DEBUG] handleSuccess for User #${user_id}, Design #${design_id}, Status: ${status}`);

        if (status !== 'success') {
            return res.status(400).json({ error: 'Payment status not successful' });
        }

        const blockFee = parseInt(process.env.BLOCK_FEE_MIN) || 500;
        let block;

        // Generate unique reference for this atomic cycle
        const cycleRef = 'CYC-' + Math.random().toString(36).substr(2, 9).toUpperCase();

        // Atomic Credit + Debit Cycle
        await db.transaction(async (trx) => {
            const wallet = await trx('wallets').where({ user_id }).first();
            if (!wallet) throw new Error('Wallet not initialized for user');

            // 1. Credit Wallet (The Payment)
            await trx('wallets').where({ user_id }).update({
                balance: wallet.balance + blockFee,
                last_updated: db.fn.now()
            });

            await trx('wallet_transactions').insert({
                wallet_id: wallet.wallet_id,
                amount: blockFee,
                type: 'credit',
                source_type: 'payment_gateway',
                description: `Top-up for design block #${design_id}`,
                reference_id: cycleRef
            });

            // 2. Trigger block creation within SAME transaction
            block = await blockService.createBlock(user_id, design_id, trx, cycleRef);
        });

        console.log(`[PAYMENT] Success: Design #${design_id} blocked for User #${user_id}`);

        res.json({
            status: 'success',
            message: 'Payment verified and Block created.',
            block_id: block.block_id,
            expiry_time: block.expiry_time
        });
    } catch (error) {
        console.error('[PAYMENT] Processing failed:', error.message);
        res.status(400).json({ error: 'Payment processing failed: ' + error.message });
    }
};
