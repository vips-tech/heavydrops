import os

PILOT_MODE = os.environ.get('PILOT_MODE', 'true').lower() == 'true'

PILOT_CONSTRAINTS = {
    'MAX_SELLERS': 25,
    'MAX_BUYERS': 1000,
    'RESTRICTED_CITY': 'Chennai',
    'ALLOW_SELF_ONBOARDING': False
}

FEATURES = {
    'AI_TRY_ON': False,
    'ONLINE_PURCHASE': False, # Core Hard Constraint: NO ECOMMERCE
    'CUSTOM_FLOW': False,
    'SELLER_INSIGHTS': False,
    'BOOST_LISTINGS': False
}

def is_feature_enabled(feature_name: str) -> bool:
    return FEATURES.get(feature_name, False)
