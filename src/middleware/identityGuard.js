const db = require('../config/db');

/**
 * Identity Guard: Enforces fresh OTP verification for critical actions.
 * Requirements: User must have verified an OTP in the last 15 minutes.
 */
exports.identityGuard = async (req, res, next) => {
    try {
        let user_id = req.user.id;
        let phone = req.user.phone;

        if (!phone) {
            const user = await db('users').where({ user_id }).first();
            phone = user?.phone;
        }

        if (!phone) {
            return res.status(401).json({ error: 'Identity verification failed: Phone not found.' });
        }

        const fifteenMinsAgo = new Date(Date.now() - 15 * 60 * 1000);

        const freshOtp = await db('otp_codes')
            .where({ phone, is_used: true }) // OTP must be used/verified
            .where('verified_at', '>=', fifteenMinsAgo)
            .first();

        if (!freshOtp) {
            return res.status(403).json({
                error: 'Identity Refresh Required',
                message: 'For your security, please verify a fresh OTP before performing this action.'
            });
        }

        next();
    } catch (error) {
        res.status(500).json({ error: 'Security guard failure' });
    }
};
