import random

import pyotp
from datetime import datetime, timedelta
import uuid


def send_opt(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    print(f"OTP is {otp}")
    return otp


def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:6]
    return code
