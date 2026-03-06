/**
 * Firebase Service for OTP Authentication
 * Handles Firebase phone authentication and push notifications
 */

const admin = require('firebase-admin');

// Initialize Firebase Admin SDK
let firebaseApp = null;

/**
 * Initialize Firebase Admin with service account
 * Note: You need to download service account key from Firebase Console
 */
function initializeFirebase() {
    if (firebaseApp) {
        return firebaseApp;
    }

    try {
        // Check if service account file exists
        const serviceAccount = require('../../firebase-service-account.json');
        
        firebaseApp = admin.initializeApp({
            credential: admin.credential.cert(serviceAccount),
            projectId: 'login-otp-29372'
        });
        
        console.log('[FIREBASE] Admin SDK initialized successfully');
        return firebaseApp;
    } catch (error) {
        console.error('[FIREBASE] Failed to initialize Admin SDK:', error.message);
        console.log('[FIREBASE] Running without Firebase Admin SDK');
        return null;
    }
}

/**
 * Send OTP via Firebase Cloud Messaging (Push Notification)
 */
async function sendOTPViaPush(deviceToken, otp, phone) {
    try {
        const app = initializeFirebase();
        if (!app) {
            throw new Error('Firebase not initialized');
        }

        const message = {
            notification: {
                title: 'Heavy Drops - Verification Code',
                body: `Your OTP is: ${otp}. Valid for 5 minutes.`
            },
            data: {
                otp: otp.toString(),
                phone: phone,
                type: 'otp_verification',
                timestamp: Date.now().toString()
            },
            token: deviceToken
        };

        const response = await admin.messaging().send(message);
        console.log(`[FIREBASE] Push notification sent successfully:`, response);
        
        return {
            success: true,
            provider: 'firebase-push',
            messageId: response
        };
    } catch (error) {
        console.error('[FIREBASE] Push notification failed:', error);
        throw error;
    }
}

/**
 * Send OTP to multiple devices (if user has multiple devices)
 */
async function sendOTPToMultipleDevices(deviceTokens, otp, phone) {
    try {
        const app = initializeFirebase();
        if (!app) {
            throw new Error('Firebase not initialized');
        }

        const messages = deviceTokens.map(token => ({
            notification: {
                title: 'Heavy Drops - Verification Code',
                body: `Your OTP is: ${otp}. Valid for 5 minutes.`
            },
            data: {
                otp: otp.toString(),
                phone: phone,
                type: 'otp_verification',
                timestamp: Date.now().toString()
            },
            token: token
        }));

        const response = await admin.messaging().sendEach(messages);
        console.log(`[FIREBASE] Sent to ${response.successCount} devices`);
        
        return {
            success: true,
            provider: 'firebase-push-multi',
            successCount: response.successCount,
            failureCount: response.failureCount
        };
    } catch (error) {
        console.error('[FIREBASE] Multi-device push failed:', error);
        throw error;
    }
}

/**
 * Verify Firebase ID Token (for client-side Firebase Auth)
 */
async function verifyFirebaseToken(idToken) {
    try {
        const app = initializeFirebase();
        if (!app) {
            throw new Error('Firebase not initialized');
        }

        const decodedToken = await admin.auth().verifyIdToken(idToken);
        console.log('[FIREBASE] Token verified for user:', decodedToken.uid);
        
        return {
            success: true,
            uid: decodedToken.uid,
            phone: decodedToken.phone_number,
            email: decodedToken.email
        };
    } catch (error) {
        console.error('[FIREBASE] Token verification failed:', error);
        throw error;
    }
}

/**
 * Create custom token for user (for seamless login)
 */
async function createCustomToken(userId, additionalClaims = {}) {
    try {
        const app = initializeFirebase();
        if (!app) {
            throw new Error('Firebase not initialized');
        }

        const customToken = await admin.auth().createCustomToken(userId.toString(), additionalClaims);
        console.log('[FIREBASE] Custom token created for user:', userId);
        
        return customToken;
    } catch (error) {
        console.error('[FIREBASE] Custom token creation failed:', error);
        throw error;
    }
}

/**
 * Send data message (silent notification with data only)
 */
async function sendDataMessage(deviceToken, data) {
    try {
        const app = initializeFirebase();
        if (!app) {
            throw new Error('Firebase not initialized');
        }

        const message = {
            data: data,
            token: deviceToken,
            android: {
                priority: 'high'
            },
            apns: {
                headers: {
                    'apns-priority': '10'
                }
            }
        };

        const response = await admin.messaging().send(message);
        console.log(`[FIREBASE] Data message sent:`, response);
        
        return {
            success: true,
            messageId: response
        };
    } catch (error) {
        console.error('[FIREBASE] Data message failed:', error);
        throw error;
    }
}

module.exports = {
    initializeFirebase,
    sendOTPViaPush,
    sendOTPToMultipleDevices,
    verifyFirebaseToken,
    createCustomToken,
    sendDataMessage
};
