const express = require('express');
const router = express.Router();
const likeController = require('../controllers/likeController');
const { verifyToken } = require('../middleware/auth');

// All like routes require authentication
router.use(verifyToken);

router.post('/toggle', likeController.toggleLike);
router.get('/me', likeController.getLikedDesigns);
router.get('/status/:id', likeController.getLikeStatus);

module.exports = router;
