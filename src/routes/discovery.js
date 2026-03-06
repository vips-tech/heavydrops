const express = require('express');
const router = express.Router();
const discoveryController = require('../controllers/discoveryController');

// GET /api/designs
router.get('/', discoveryController.getCuratedDesigns);

// GET /api/designs/:id
router.get('/:id', discoveryController.getDesignById);

module.exports = router;
