const db = require('../config/db');
const jwt = require('jsonwebtoken');
const smsService = require('../services/smsService');

/**
 * Request OTP for Login/Register
 */
exports.requestOTP = async (req, res) => {
    try {
        const { phone } = req.body;
        if (!phone) return res.status(400).json({ error: 'Phone number required' });

        // Generate 6-digit OTP
        const code = Math.floor(100000 + Math.random() * 900000).toString();
        const expiresAt = new Date(Date.now() + 5 * 60 * 1000); // 5 mins

        await db('otp_codes').insert({
            phone,
            code,
            expires_at: expiresAt
        });

        // Send OTP via SMS
        const smsResult = await smsService.sendOTP(phone, code);
        
        console.log(`[AUTH] OTP for ${phone}: ${code} (Expires: ${expiresAt})`);
        console.log(`[AUTH] SMS Status:`, smsResult);
        
        res.json({ 
            message: 'OTP sent successfully', 
            phone,
            smsProvider: smsResult.provider
        });
    } catch (error) {
        console.error('[AUTH] OTP request failed:', error);
        res.status(500).json({ error: 'Failed to generate OTP' });
    }
};

/**
 * Verify OTP and Register/Login User
 */
exports.verifyOTP = async (req, res) => {
    try {
        const { phone, code } = req.body;
        console.log(`[AUTH] DEBUG: phone=${phone}, code=${code}, type=${typeof code}`);

        // Master OTP for Automated Testing
        if (code == '123456') {
            console.log(`[AUTH] Master OTP bypass used for ${phone}`);
        } else {
            const validOTP = await db('otp_codes')
                .where({ phone, code, is_used: false })
                .where('expires_at', '>', new Date())
                .orderBy('created_at', 'desc')
                .first();

            if (!validOTP) {
                return res.status(401).json({ error: 'Invalid or expired OTP' });
            }

            // Mark OTP as used and verified
            await db('otp_codes').where({ otp_id: validOTP.otp_id }).update({
                is_used: true,
                verified_at: db.fn.now()
            });
        }

        // Find or Create User
        let user = await db('users').where({ phone }).first();
        if (!user) {
            const [userId] = await db('users').insert({
                phone,
                role: 'buyer',
                status: 'active',
                active_block_count: 0
            }, ['user_id']);
            user = { user_id: userId, role: 'buyer', phone, status: 'active', active_block_count: 0 };

            // Create wallet for new user
            await db('wallets').insert({ user_id: user.user_id, balance: 1000 });
        }

        const token = jwt.sign({ id: user.user_id, role: user.role, phone: user.phone }, process.env.JWT_SECRET);
        res.json({ token, user_id: user.user_id, role: user.role, message: 'Authentication successful' });
    } catch (error) {
        console.error('[AUTH] Verification failed:', error);
        res.status(500).json({ error: 'Verification failed' });
    }
};

/**
 * Admin Login with Credentials
 */
exports.adminLogin = async (req, res) => {
    try {
        const { username, password } = req.body;
        
        // Simple credential check (in production, use hashed passwords)
        if (username === 'admin' && password === 'admin') {
            // Find or create admin user
            let admin = await db('users').where({ role: 'admin' }).first();
            
            if (!admin) {
                const [userId] = await db('users').insert({
                    phone: 'admin@heavydrops.com',
                    role: 'admin',
                    status: 'active',
                    active_block_count: 0,
                    name: 'Administrator'
                }, ['user_id']);
                admin = { user_id: userId, role: 'admin', phone: 'admin@heavydrops.com', status: 'active' };
            }

            const token = jwt.sign(
                { id: admin.user_id, role: admin.role, phone: admin.phone }, 
                process.env.JWT_SECRET
            );
            
            res.json({ 
                token, 
                user_id: admin.user_id, 
                role: admin.role, 
                message: 'Admin authentication successful' 
            });
        } else {
            res.status(401).json({ error: 'Invalid admin credentials' });
        }
    } catch (error) {
        console.error('[AUTH] Admin login failed:', error);
        res.status(500).json({ error: 'Admin login failed' });
    }
};

exports.getMe = async (req, res) => {
    try {
        const user = await db('users').where({ user_id: req.user.id }).first();
        if (!user) return res.status(404).json({ error: 'User not found' });
        res.json({
            user_id: user.user_id,
            role: user.role,
            phone: user.phone,
            name: user.name,
            status: user.status,
            active_block_count: user.active_block_count
        });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch session data' });
    }
};

/**
 * Verify Firebase ID Token and create session
 */
exports.verifyFirebaseToken = async (req, res) => {
    try {
        const { idToken, phone } = req.body;
        
        if (!idToken) {
            return res.status(400).json({ error: 'Firebase ID token required' });
        }

        // Verify Firebase token
        const firebaseService = require('../services/firebaseService');
        const verificationResult = await firebaseService.verifyFirebaseToken(idToken);

        if (!verificationResult.success) {
            return res.status(401).json({ error: 'Invalid Firebase token' });
        }

        // Find or create user
        let user = await db('users').where({ phone: verificationResult.phone || phone }).first();
        
        if (!user) {
            const [userId] = await db('users').insert({
                phone: verificationResult.phone || phone,
                role: 'buyer',
                status: 'active',
                active_block_count: 0
            }, ['user_id']);
            
            user = { 
                user_id: userId, 
                role: 'buyer', 
                phone: verificationResult.phone || phone, 
                status: 'active' 
            };

            // Create wallet for new user
            await db('wallets').insert({ user_id: user.user_id, balance: 1000 });
        }

        // Create JWT token
        const token = jwt.sign(
            { id: user.user_id, role: user.role, phone: user.phone }, 
            process.env.JWT_SECRET
        );

        console.log(`[AUTH] Firebase user authenticated: ${user.phone}`);
        
        res.json({ 
            token, 
            user_id: user.user_id, 
            role: user.role, 
            message: 'Firebase authentication successful' 
        });
    } catch (error) {
        console.error('[AUTH] Firebase verification failed:', error);
        res.status(500).json({ error: 'Firebase verification failed' });
    }
};

/**
 * Save FCM device token for push notifications
 */
exports.saveFCMToken = async (req, res) => {
    try {
        const { token: fcmToken } = req.body;
        const userId = req.user?.id;

        if (!fcmToken) {
            return res.status(400).json({ error: 'FCM token required' });
        }

        // Create device_tokens table if it doesn't exist (you may need to add migration)
        // For now, we'll store in a simple way
        await db('device_tokens').insert({
            user_id: userId || null,
            fcm_token: fcmToken,
            platform: 'web',
            created_at: db.fn.now()
        }).onConflict(['fcm_token']).merge();

        console.log(`[AUTH] FCM token saved for user: ${userId}`);
        res.json({ message: 'FCM token saved successfully' });
    } catch (error) {
        console.error('[AUTH] Failed to save FCM token:', error);
        res.status(500).json({ error: 'Failed to save FCM token' });
    }
};

/**
 * Public Application for Jewellers
 */
exports.registerSeller = async (req, res) => {
    try {
        const { business_name, email, city, brand_story } = req.body;

        // Check for existing
        const existing = await db('sellers').where({ email }).first();
        if (existing) return res.status(400).json({ error: 'Email already registered' });

        // Insert applicant
        await db('sellers').insert({
            business_name,
            email,
            city,
            membership_status: 'applicant'
        });

        console.log(`[CURATION] New Seller Application: ${business_name} in ${city}`);
        res.json({ message: 'Application submitted for audit.' });
    } catch (error) {
        res.status(500).json({ error: 'Application failed' });
    }
};
