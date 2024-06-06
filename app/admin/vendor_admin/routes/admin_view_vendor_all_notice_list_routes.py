
from flask import Blueprint
from app.admin.vendor_admin.services.admin_view_vendor_all_notice_as_list import get_vendor_all_notices, get_vendor_single_notices
from utils.decorator.auth_checker import admin_token_authentication

admin_vendor_all_notice_list_routes = Blueprint("admin_vendor_all_notice_list_routes", __name__)

#----------------------------------  Topics : Admin_view_vendor_all_notice, Author: Md. Iquball Hossain, Date: 03-12-2023 -------------------------------------

@admin_vendor_all_notice_list_routes.route("/view_vendor_all_notice", methods=["GET"])
@admin_token_authentication()
def admin_view_vendors_all_notice(current_admin):
    return get_vendor_all_notices(current_admin)

#----------------------------------  Topics : Admin_view_vendor_single_notice, Author: Md. Iquball Hossain, Date: 03-12-2023 -------------------------------------

@admin_vendor_all_notice_list_routes.route("/view_vendor_single_notice/<int:vendor_id>", methods=["GET"])
@admin_token_authentication()
def admin_view_vendors_single_notice(current_admin,vendor_id):
    return get_vendor_single_notices(current_admin,vendor_id)