const express = require('express');
const router = express.Router();
const appointmentController = require('../controllers/appointmentController');
const { identityGuard } = require('../middleware/identityGuard');
const rateLimiter = require('../middleware/rateLimiter');
const { maintenanceGate } = require('../middleware/maintenanceMode');
const auth = require('../middleware/auth');

// PROTECTED ROUTES (SESSION-BASED)
router.use(auth.verifyToken);

// POST /api/appointments - Book a visit (Identity Guard Required)
router.post('/', rateLimiter.bridgeLimiter, maintenanceGate, identityGuard, appointmentController.bookAppointment);
router.patch('/:appointment_id/status', maintenanceGate, appointmentController.updateAppointmentStatus);

module.exports = router;
