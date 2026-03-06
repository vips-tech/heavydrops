const express = require('express');
const router = express.Router();
const intentController = require('../controllers/intentController');
const { identityGuard } = require('../middleware/identityGuard');
const rateLimiter = require('../middleware/rateLimiter');
const { maintenanceGate } = require('../middleware/maintenanceMode');
const auth = require('../middleware/auth');

// PROTECTED ROUTES (SESSION-BASED)
router.use(auth.verifyToken);

// POST /api/blocks - Create intent block (Identity Guard Required)
router.post('/', rateLimiter.intentLimiter, maintenanceGate, identityGuard, intentController.createIntentBlock);

// GET /api/wallets/:userId - View wallet and activity
router.get('/:userId', intentController.getWallet);

// GET /api/blocks/ledger/:userId - Detailed transaction ledger
router.get('/ledger/:userId', intentController.getLedger);

// GET /api/blocks/status/:designId - Check block state for a design
router.get('/status/:designId', intentController.getBlockStatus);

module.exports = router;
