import os
import requests
from twilio.rest import Client

def get_twilio_client():
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    if account_sid and auth_token:
        return Client(account_sid, auth_token)
    return None

def send_via_twilio(phone, otp):
    client = get_twilio_client()
    if not client:
        raise ValueError('Twilio credentials not configured')
    
    try:
        message = client.messages.create(
            body=f"Your Heavy Drops verification code is: {otp}. Valid for 5 minutes.",
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            to=phone
        )
        print(f"[SMS] Twilio message sent: {message.sid}")
        return {'success': True, 'provider': 'twilio', 'messageId': message.sid}
    except Exception as e:
        print(f"[SMS] Twilio error: {str(e)}")
        raise e

def send_via_msg91(phone, otp):
    auth_key = os.environ.get('MSG91_AUTH_KEY')
    if not auth_key:
        raise ValueError('MSG91 credentials not configured')
        
    try:
        clean_phone = phone.replace('+', '').replace(' ', '')
        print(f"[SMS] MSG91 sending to: {clean_phone}, OTP: {otp}")
        
        template_id = os.environ.get('MSG91_TEMPLATE_ID')
        
        if template_id and template_id != 'paste_your_template_id_here':
            response = requests.get('https://api.msg91.com/api/v5/otp', params={
                'authkey': auth_key,
                'mobile': clean_phone,
                'otp': otp,
                'template_id': template_id
            })
            print(f"[SMS] MSG91 response:", response.json())
            return {'success': True, 'provider': 'msg91', 'response': response.json()}
        else:
            flow_id = os.environ.get('MSG91_FLOW_ID', '')
            sender = os.environ.get('MSG91_SENDER_ID', 'MSGIND')
            response = requests.post('https://control.msg91.com/api/v5/flow/', json={
                'flow_id': flow_id,
                'sender': sender,
                'mobiles': clean_phone,
                'VAR1': otp,
                'VAR2': '5'
            }, headers={
                'authkey': auth_key,
                'content-type': 'application/json'
            })
            print(f"[SMS] MSG91 response:", response.json())
            return {'success': True, 'provider': 'msg91', 'response': response.json()}
    except Exception as e:
        print(f"[SMS] MSG91 error: {str(e)}")
        raise e

def send_via_fast2sms(phone, otp):
    api_key = os.environ.get('FAST2SMS_API_KEY')
    if not api_key:
        raise ValueError('Fast2SMS credentials not configured')
        
    try:
        number = phone.replace('+91', '')
        sender_id = os.environ.get('FAST2SMS_SENDER_ID', 'TXTIND')
        response = requests.post('https://www.fast2sms.com/dev/bulkV2', json={
            'route': 'otp',
            'sender_id': sender_id,
            'message': f"Your Heavy Drops OTP is {otp}. Valid for 5 minutes.",
            'variables_values': otp,
            'flash': 0,
            'numbers': number
        }, headers={
            'authorization': api_key,
            'Content-Type': 'application/json'
        })
        print(f"[SMS] Fast2SMS message sent to {phone}")
        return {'success': True, 'provider': 'fast2sms', 'response': response.json()}
    except Exception as e:
        print(f"[SMS] Fast2SMS error: {str(e)}")
        raise e

def send_otp(phone, otp):
    provider = os.environ.get('SMS_PROVIDER', 'console').lower()
    print(f"[SMS] Sending OTP {otp} to {phone} via {provider}")
    
    try:
        if provider == 'twilio':
            return send_via_twilio(phone, otp)
        elif provider == 'msg91':
            return send_via_msg91(phone, otp)
        elif provider == 'fast2sms':
            return send_via_fast2sms(phone, otp)
        else:
            print(f"[SMS] ========================================")
            print(f"[SMS] OTP for {phone}: {otp}")
            print(f"[SMS] ========================================")
            return {'success': True, 'provider': 'console', 'otp': otp}
    except Exception as e:
        print(f"[SMS] Failed to send via {provider}, falling back to console")
        print(f"[SMS] ========================================")
        print(f"[SMS] OTP for {phone}: {otp}")
        print(f"[SMS] ========================================")
        return {'success': True, 'provider': 'console-fallback', 'otp': otp, 'error': str(e)}
