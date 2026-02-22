import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    """Generate 6 digit OTP"""
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    """Send OTP to user email"""

    subject = "Login OTP Verification"

    message = f"""
Hello,
Your TODO App login OTP is: {otp}
This OTP expires in 3 minutes.
Do not share it with anyone.
Regards,
TODO App Team
"""
    from_email = f"TODO App <{settings.EMAIL_HOST_USER}>"

    send_mail(
        subject,
        message,
        from_email,
        [email],
        fail_silently=False,
    )