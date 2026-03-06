const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const { authLimiter } = require('../middleware/rateLimiter');
const auth = require('../middleware/auth');

router.post('/request-otp', authController.requestOTP);
router.post('/verify-otp', authController.verifyOTP);
router.post('/admin-login', authController.adminLogin);
router.post('/register-seller', authController.registerSeller);
router.get('/me', auth.verifyToken, authController.getMe);

// Firebase Authentication Routes
router.post('/firebase-verify', authController.verifyFirebaseToken);
router.post('/save-fcm-token', authController.saveFCMToken);

module.exports = router;
