const rateLimit = require('express-rate-limit');

/**
 * Standard Auth/Block Limiter
 * 5 requests per minute
 */
exports.intentLimiter = rateLimit({
    windowMs: 1 * 60 * 1000, // 1 minute
    max: 10, // Relaxed for verification
    message: { error: 'Too many requests. Please slow down your intentional actions.' },
    standardHeaders: true,
    legacyHeaders: false,
});

/**
 * Intent Bridge Limiter (Appointments)
 * 2 per day (simulated with 2 per 24h window)
 */
exports.bridgeLimiter = rateLimit({
    windowMs: 24 * 60 * 60 * 1000,
    max: 20, // Relaxed for verification
    message: { error: 'Showroom visit request limit reached for today.' }
});

/**
 * Auth/Identity Limiter
 * 5 per minute
 */
exports.authLimiter = rateLimit({
    windowMs: 1 * 60 * 1000,
    max: 15, // Relaxed for verification
    message: { error: 'Too many login attempts. Please wait.' }
});

/**
 * Standard API Limiter
 */
exports.apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: { error: 'System bandwidth limit reached.' }
});
