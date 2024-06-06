# Author: Shidul Islam
# Date: 07-11-2023
# */

from utils.lib.lib import otp_generate
from utils.miscellaneous.constants import VERIFY_USER, VERIFY_ADMIN, VERIFY_VENDOR
from app.external.utils.verify_user import verify_user
from app.external.utils.match_otp import match_otp


def send_otp_service(req):
    try:
        body = req
        email, type = body.get("email"), body.get("type")
        otp = otp_generate(5)
        if (type == VERIFY_USER):
            return verify_user(email, otp)
    except Exception as e:
        raise Exception(e)


def match_otp_service(req):
    try:
        body = req
        email, type, otp = body.get("email"), body.get(
            "type"), body.get("otp")
        if (type == VERIFY_USER):
            return match_otp(email, type, otp)
    except Exception as e:
        raise Exception(e)
