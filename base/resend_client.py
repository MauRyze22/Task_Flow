import resend
from django.conf import settings


def get_resend_client():
    resend.api_key = settings.RESEND_API_KEY
    return resend
