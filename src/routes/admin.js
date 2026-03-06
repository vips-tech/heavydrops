const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');
const auth = require('../middleware/auth');
const { sellerCapGuard } = require('../middleware/pilotGuard');

// Apply Global Admin Gating
router.use(auth.verifyToken, auth.authorize(['admin']));

// GET /api/admin/stats - Master statistics
router.get('/stats', adminController.getStats);

// POST /api/admin/wallet/adjust - Adjust wallet balance
router.post('/wallet/adjust', adminController.adjustWallet);

// User Management
router.get('/users', adminController.getUsers);
router.patch('/users/:user_id/status', adminController.updateUserStatus);

// Operational Monitoring
router.get('/appointments', adminController.getAppointmentsSummary);
router.get('/blocks', adminController.getAllBlocks);

// Violation Desk
router.post('/violations', adminController.logViolation);
router.get('/violations', adminController.getViolations);

// Design Photography Audit
router.get('/designs/pending', adminController.getPendingDesigns);
router.patch('/designs/:design_id/approve', adminController.approveListing);
router.get('/designs/media/pending', adminController.getPendingMedia);
router.post('/designs/media/:media_id/review', adminController.reviewDesignMedia);

// Seller Management
router.get('/sellers', adminController.getSellers);
router.patch('/sellers/:seller_id/status', sellerCapGuard, adminController.updateSellerStatus);

// Gold Rate Reference System
router.get('/gold-rate', adminController.getGoldRate);
router.post('/gold-rate', adminController.updateGoldRate);

module.exports = router;
