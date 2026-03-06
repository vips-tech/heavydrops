const express = require('express');
const router = express.Router();
const healthController = require('../controllers/healthController');
const auth = require('../middleware/auth');

// GET /api/health/telemetry - Admin health check
router.get('/telemetry', auth.verifyToken, auth.authorize(['admin']), healthController.getSystemHealth);

// GET /api/health/config - Public feature flags & mode
router.get('/config', healthController.getSystemConfig);

module.exports = router;
