
#---------------------------------- Topics : view vendor notice form admin API Endpoint, Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------------------------

from flask import Blueprint
from app.vendor.services.vendor_notice_view_service import vendor_notice_from_admin, vendor_special_notice_from_admin
from utils.decorator.auth_checker import vendor_token_authentication

vendor_notice_view_routes = Blueprint("vendor_notice_view_routes", __name__)

#----------------------------------  Topics : view vendor notice form admin API Endpoint, Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------------------------

@vendor_notice_view_routes.route("/view_vendor_notice", methods=["GET"])
@vendor_token_authentication()
def vendor_notice_view(current_vendor):
    return vendor_notice_from_admin(current_vendor)

#----------------------------------  Topics : view vendor notice form admin as last moth and any year API Endpoint, Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------------------------

@vendor_notice_view_routes.route("/vendor_view_specific_notice", methods=["GET"])
@vendor_token_authentication()
def vendor_special_notice_view(current_vendor):
    return vendor_special_notice_from_admin(current_vendor)