
from flask import Blueprint, g, request
import app
from app.admin.vendor_admin.services.admin_view_vendor_profile_as_list import get_all_vendor_profiles, get_vendor_single_profile,get_profiles_by_business_category, get_pending_vendor_profiles
from utils.decorator.auth_checker import admin_token_authentication

admin_vendor_profile_list_routes = Blueprint("admin_vendor_profile_list_routes", __name__)

#------------------------  Topics : Admin vendor all profile list routes, Author: Md. Iquball Hossain, Date: 03-12-2023 --------------------

@admin_vendor_profile_list_routes.route("/view_vendors_all_profile", methods=["GET"])
@admin_token_authentication()
def admin_view_vendors_all_profile(current_admin):
    return get_all_vendor_profiles(current_admin)

#-----------------------  Topics : Admin vendor single profile list using id routes, Author: Md. Iquball Hossain, Date: 03-12-2023 ---------------------

@admin_vendor_profile_list_routes.route("/view_vendors_single_profile_id/<int:vendor_id>", methods=["GET"])
@admin_token_authentication()
def admin_view_vendors_single_profile_vendor_id(current_admin,vendor_id):
    return get_vendor_single_profile(current_admin,vendor_id)

#----------- Topics : Admin view vendor single profile list using business category, Author: Md. Iquball Hossain, Date: 12-12-2023 ---------------

@admin_vendor_profile_list_routes.route("/view_vendor_profiles_by_category/<string:business_category>", methods=["GET"])
@admin_token_authentication()
def view_vendor_profiles_by_category(current_admin, business_category):
    return get_profiles_by_business_category(current_admin, business_category)

#----------- Topics : Admin view vendor profile list using profile status , Author: Md. Iquball Hossain, Date: 12-12-2023 ---------------

@admin_vendor_profile_list_routes.route("/pending_vendor_profiles/<string:vendor_profile_status>", methods=["GET"])
@admin_token_authentication()
def view_pending_vendor_profiles(current_admin, vendor_profile_status):
    return get_pending_vendor_profiles(current_admin, vendor_profile_status)