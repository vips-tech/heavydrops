const express = require('express');
const router = express.Router();
const paymentController = require('../controllers/paymentController');
const auth = require('../middleware/auth');

router.post('/initiate', auth.verifyToken, require('../middleware/identityGuard').identityGuard, paymentController.initiatePayment);
router.post('/callback', auth.verifyToken, require('../middleware/identityGuard').identityGuard, paymentController.handleSuccess);

module.exports = router;
