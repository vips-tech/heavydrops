/**
 * Messaging Service
 * Stubs for SMS and Email integrations.
 */
class MessagingService {
    async sendSMS(userId, message) {
        // Mock SMS Gateway
        console.log(`[GATEWAY] [SMS] User #${userId}: "${message}"`);
        return true;
    }

    async sendEmail(userId, message) {
        // Mock Email SMTP
        console.log(`[GATEWAY] [EMAIL] User #${userId}: "${message}"`);
        return true;
    }

    async sendInApp(userId, message) {
        // Mock Web Push or Socket.io
        console.log(`[GATEWAY] [IN-APP] User #${userId}: "${message}"`);
        return true;
    }
}

module.exports = new MessagingService();
