/**
 * SMS Service for sending OTP
 * Supports multiple providers: Twilio, MSG91, Fast2SMS
 */

const twilio = require('twilio');

// Initialize Twilio client (if credentials are provided)
let twilioClient = null;
if (process.env.TWILIO_ACCOUNT_SID && process.env.TWILIO_AUTH_TOKEN) {
    twilioClient = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);
}

/**
 * Send OTP via Twilio
 */
async function sendViaTwilio(phone, otp) {
    if (!twilioClient) {
        throw new Error('Twilio credentials not configured');
    }

    try {
        const message = await twilioClient.messages.create({
            body: `Your Heavy Drops verification code is: ${otp}. Valid for 5 minutes.`,
            from: process.env.TWILIO_PHONE_NUMBER,
            to: phone
        });
        console.log(`[SMS] Twilio message sent: ${message.sid}`);
        return { success: true, provider: 'twilio', messageId: message.sid };
    } catch (error) {
        console.error('[SMS] Twilio error:', error.message);
        throw error;
    }
}

/**
 * Send OTP via MSG91 (Popular in India)
 */
async function sendViaMSG91(phone, otp) {
    const axios = require('axios');
    
    if (!process.env.MSG91_AUTH_KEY) {
        throw new Error('MSG91 credentials not configured');
    }

    try {
        // Clean phone number - remove + and spaces
        const cleanPhone = phone.replace(/[\s+]/g, '');
        
        console.log(`[SMS] MSG91 sending to: ${cleanPhone}, OTP: ${otp}`);
        
        // Use template if available, otherwise use direct OTP route
        const templateId = process.env.MSG91_TEMPLATE_ID;
        
        if (templateId && templateId !== 'paste_your_template_id_here') {
            // Use template-based sending
            const response = await axios.get('https://api.msg91.com/api/v5/otp', {
                params: {
                    authkey: process.env.MSG91_AUTH_KEY,
                    mobile: cleanPhone,
                    otp: otp,
                    template_id: templateId
                }
            });
            
            console.log(`[SMS] MSG91 response:`, response.data);
            return { success: true, provider: 'msg91', response: response.data };
        } else {
            // Use direct SMS API (works better without template)
            const response = await axios.post(
                'https://control.msg91.com/api/v5/flow/',
                {
                    flow_id: process.env.MSG91_FLOW_ID || '',
                    sender: process.env.MSG91_SENDER_ID || 'MSGIND',
                    mobiles: cleanPhone,
                    VAR1: otp,
                    VAR2: '5'
                },
                {
                    headers: {
                        'authkey': process.env.MSG91_AUTH_KEY,
                        'content-type': 'application/json'
                    }
                }
            );
            
            console.log(`[SMS] MSG91 response:`, response.data);
            return { success: true, provider: 'msg91', response: response.data };
        }
    } catch (error) {
        console.error('[SMS] MSG91 error:', error.response?.data || error.message);
        throw error;
    }
}

/**
 * Send OTP via Fast2SMS (Indian SMS provider)
 */
async function sendViaFast2SMS(phone, otp) {
    const axios = require('axios');
    
    if (!process.env.FAST2SMS_API_KEY) {
        throw new Error('Fast2SMS credentials not configured');
    }

    try {
        const response = await axios.post('https://www.fast2sms.com/dev/bulkV2', {
            route: 'otp',
            sender_id: process.env.FAST2SMS_SENDER_ID || 'TXTIND',
            message: `Your Heavy Drops OTP is ${otp}. Valid for 5 minutes.`,
            variables_values: otp,
            flash: 0,
            numbers: phone.replace('+91', '')
        }, {
            headers: {
                'authorization': process.env.FAST2SMS_API_KEY,
                'Content-Type': 'application/json'
            }
        });
        
        console.log(`[SMS] Fast2SMS message sent to ${phone}`);
        return { success: true, provider: 'fast2sms', response: response.data };
    } catch (error) {
        console.error('[SMS] Fast2SMS error:', error.message);
        throw error;
    }
}

/**
 * Main function to send OTP
 * Tries configured provider, falls back to console logging
 */
async function sendOTP(phone, otp) {
    const provider = process.env.SMS_PROVIDER || 'console';
    
    console.log(`[SMS] Sending OTP ${otp} to ${phone} via ${provider}`);
    
    try {
        switch (provider.toLowerCase()) {
            case 'twilio':
                return await sendViaTwilio(phone, otp);
            
            case 'msg91':
                return await sendViaMSG91(phone, otp);
            
            case 'fast2sms':
                return await sendViaFast2SMS(phone, otp);
            
            case 'console':
            default:
                // Console-only mode (for development/testing)
                console.log(`[SMS] ========================================`);
                console.log(`[SMS] OTP for ${phone}: ${otp}`);
                console.log(`[SMS] ========================================`);
                return { success: true, provider: 'console', otp };
        }
    } catch (error) {
        // Fallback to console if SMS fails
        console.error(`[SMS] Failed to send via ${provider}, falling back to console`);
        console.log(`[SMS] ========================================`);
        console.log(`[SMS] OTP for ${phone}: ${otp}`);
        console.log(`[SMS] ========================================`);
        return { success: true, provider: 'console-fallback', otp, error: error.message };
    }
}

module.exports = {
    sendOTP
};
