#---------------------------------- Topics : vendor profile all Endpoint, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

from flask import Blueprint
# from app.vendor.validators.update_vendor_profile_validator import UpdateVendorProfileValidator
from app.vendor.services.vender_profile_service import update_vendor_profile, view_vendor_profile, delete_vendor_profile
from utils.decorator.auth_checker import vendor_token_authentication

vendor_profile_routes = Blueprint("vendor_profile_routes", __name__)

#----------------------------------  Topics : vendor profile view (get) Endpoint, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

@vendor_profile_routes.route("/view_vendor_profile", methods=["GET"])
@vendor_token_authentication()
def vendor_profile(current_vendor):
    return view_vendor_profile(current_vendor)

#----------------------------------  Topics : vendor profile edit/update (put) Endpoint, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

@vendor_profile_routes.route("/update_vendor_profile", methods=["PUT"])
@vendor_token_authentication()
def update_vendor(current_vendor):
    return update_vendor_profile(current_vendor)

#----------------------------------  Topics : vendor profile delete for admin (delete) Endpoint, Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------------------------   

@vendor_profile_routes.route("/delete_vendor_profile", methods=["DELETE"])
@vendor_token_authentication()
def delete_vendor(current_vendor):
    return delete_vendor_profile(current_vendor)