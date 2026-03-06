from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# We will attach this limiter to the app in app.py later
limiter = Limiter(
    key_func=get_remote_address,
    # Need to be explicitly configured at app init
    default_limits=["100 per 15 minutes"]
)

# Standard Auth/Block Limiter 
def intent_limiter():
    return limiter.limit("10 per 1 minute", error_message='Too many requests. Please slow down your intentional actions.')

# Intent Bridge Limiter (Appointments)
def bridge_limiter():
    return limiter.limit("20 per 1 day", error_message='Showroom visit request limit reached for today.')

# Auth/Identity Limiter
def auth_limiter():
    return limiter.limit("15 per 1 minute", error_message='Too many login attempts. Please wait.')

def api_limiter():
    return limiter.limit("100 per 15 minutes", error_message='System bandwidth limit reached.')
