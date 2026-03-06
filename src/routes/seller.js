const express = require('express');
const router = express.Router();
const sellerController = require('../controllers/sellerController');
const auth = require('../middleware/auth');
const upload = require('../config/uploadConfig');

router.get('/profile/:sellerId', sellerController.getSellerProfile);
router.get('/me', auth.verifyToken, auth.authorize(['seller', 'admin']), sellerController.getMySellerProfile);
router.get('/dashboard/:sellerId', auth.verifyToken, auth.authorize(['seller', 'admin']), sellerController.getDashboardData);
router.get('/performance/:sellerId', auth.verifyToken, auth.authorize(['seller', 'admin']), sellerController.getDesignPerformance);
router.post('/appointments/:appointment_id/outcome', auth.verifyToken, auth.authorize(['seller', 'admin']), sellerController.markAppointmentOutcome);
router.patch('/designs/:designId', auth.verifyToken, auth.authorize(['seller', 'admin']), sellerController.updateDesign);

// Photography Standardization Endpoint
router.post('/designs/:designId/media',
    auth.verifyToken,
    auth.authorize(['seller']),
    upload.array('images', 5),
    sellerController.uploadDesignMedia
);

module.exports = router;
