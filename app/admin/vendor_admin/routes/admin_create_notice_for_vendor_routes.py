
from flask import Blueprint
from app.admin.vendor_admin.services.admin_create_notice_for_vendor_service import create_notice_for_vendor, update_notice_for_vendor, delete_notice_for_vendor, get_notices_for_admin
from utils.decorator.auth_checker import admin_token_authentication

admin_create_notice_for_vendor_routes = Blueprint("vendor_notices_admin_routes", __name__)

#----------------------------------  Topics : Admin create notice for vendor API Endpoint, Author: Md. Iquball Hossain, Date: 27-11-2023----------------------

@admin_create_notice_for_vendor_routes.route("/create_vendor_notice", methods=["POST"])
@admin_token_authentication()
def create_vendor_notice(current_admin):
    return create_notice_for_vendor(current_admin)

#----------------------------------  Topics : admin view all their personal notice, Author: Md. Iquball Hossain, Date: 27-11-2023 ----------------------

@admin_create_notice_for_vendor_routes.route("/admin_view_vendor_notice", methods=["GET"])
@admin_token_authentication()
def view_personal_vendor_notice(current_admin):
    return get_notices_for_admin(current_admin)

#----------------------------------  Topics : Admin create notice for vendor API Endpoint, Author: Md. Iquball Hossain, Date: 27-11-2023 ----------------------

@admin_create_notice_for_vendor_routes.route("/update_vendor_notice/<int:notice_id>", methods=["PUT"])
@admin_token_authentication()
def update_vendor_notice(current_admin,notice_id):
    return update_notice_for_vendor(current_admin,notice_id)

#----------------------------------  Topics : Admin create notice for vendor API Endpoint, Author: Md. Iquball Hossain, Date: 28-11-2023 ------------------------   

@admin_create_notice_for_vendor_routes.route("/delete_vendor_notice/<int:notice_id>", methods=["DELETE"])
@admin_token_authentication()
def delete_vendor_notice(current_admin,notice_id):
    return delete_notice_for_vendor(current_admin,notice_id)