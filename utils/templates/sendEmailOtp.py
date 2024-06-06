from utils.miscellaneous.constants import PROJECT_NAME, PROJECT_URL


def send_email_otp(otp, otp_for):
    return F"""
    {otp} is your One Time Password (OTP) from {PROJECT_NAME} for {otp_for}.
    Validity for OTP is 5 minutes.
    Note: Please do not share your OTP with anyone.
    For more information {PROJECT_URL}

    Thanks.
    """
