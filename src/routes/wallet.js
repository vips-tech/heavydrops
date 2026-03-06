const express = require('express');
const router = express.Router();
const walletController = require('../controllers/walletController');
const auth = require('../middleware/auth');

// PROTECTED ROUTES
router.use(auth.verifyToken);

// GET /api/wallet - Get high-level wallet info
router.get('/', walletController.getWalletInfo);

// GET /api/wallet/transactions - Get detailed ledger
router.get('/transactions', walletController.getLedger);

module.exports = router;
