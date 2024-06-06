from flask import Blueprint
from app.admin.vendor_admin.services.admin_delete_vendor_profile_service import delete_vendor_profile,admin_update_vendor_profile
from utils.decorator.auth_checker import admin_token_authentication

admin_delete_vendor_profile_routes = Blueprint("admin_delete_vendor_profile_routes", __name__)

#----------------------------------  Topics : vendor profile delete for admin (delete) Endpoint, Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------------------------   

@admin_delete_vendor_profile_routes.route("/admin_edit_vendor_profile/<int:vendor_id>", methods=["PUT"])
@admin_token_authentication()
def admin_edit_vendor(current_admin,vendor_id):
    return admin_update_vendor_profile(current_admin,vendor_id)


@admin_delete_vendor_profile_routes.route("/delete_vendor_profile/<int:vendor_id>", methods=["DELETE"])
@admin_token_authentication()
def delete_vendor(current_admin,vendor_id):
    return delete_vendor_profile(current_admin,vendor_id)