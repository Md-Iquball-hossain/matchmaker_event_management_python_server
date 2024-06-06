from flask import Blueprint
from app.admin.vendor_admin.services.admin_vendor_service import admin_view_vendor_service, admin_view_single_vendor_service, admin_change_vendor_service_permission

from utils.decorator.auth_checker import admin_token_authentication

admin_vendor_service = Blueprint("admin_vendor_service", __name__)

#------------------------  Topics : Admin vendor all profile list routes, Author: Md. Iquball Hossain, Date: 21-12-2023 --------------------

@admin_vendor_service.route("/admin_view_vendor_services_list", methods=["GET"])
@admin_token_authentication()
def admin_view_vendors_all_profile(current_admin):
    return admin_view_vendor_service(current_admin)

#-----------------------  Topics : Admin vendor single profile list using id routes, Author: Md. Iquball Hossain, Date: 03-12-2023 ---------------------

@admin_vendor_service.route("/admin_view_single_vendor_service_from_list/<int:vendor_service_id>", methods=["GET"])
@admin_token_authentication()
def admin_view_vendors_single_service(current_admin,vendor_service_id):
    return admin_view_single_vendor_service(current_admin,vendor_service_id)

#-----------------------  Topics : Admin accept vendor's single service list using vendor service id routes, Author: Md. Iquball Hossain, Date: 21-12-2023 ---------------------

@admin_vendor_service.route("/admin_change_vendor_service_permission/<int:vendor_service_id>", methods=["PUT"])
@admin_token_authentication()
def admin_edit_vendors_single_service(current_admin,vendor_service_id):
    return admin_change_vendor_service_permission(current_admin,vendor_service_id)