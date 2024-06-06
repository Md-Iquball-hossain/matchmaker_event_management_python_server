
#---------------------- Topics : vendor profile all Endpoint, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

from flask import Blueprint
from app.admin.user_admin.services.user_service import get_user_list,get_user_single, get_user_profiles_by_gender
from utils.decorator.auth_checker import admin_token_authentication

admin_user_routes = Blueprint("admin_user_routes", __name__)

#-------------------------  Topics : user profile list view (get) Endpoint, Author: Md. Iquball Hossain, Date: 12-11-2023 -------------------------------------

@admin_user_routes.route("/view_user_list", methods=["GET"])
@admin_token_authentication()
def user_list_all(current_admin):
    return get_user_list(current_admin)

#-----------------------  Topics : user profile list view (get) Endpoint, Author: Md. Iquball Hossain, Date: 12-11-2023 -------------------------------------

@admin_user_routes.route("/view_single_user_list/<int:id>", methods=["GET"])
@admin_token_authentication()
def user_list_single(current_admin, id):
    return get_user_single(current_admin, id)

#-----------------------  Topics : user profile list view as gender (get) Endpoint, Author: Md. Iquball Hossain, Date: 13-11-2023 -------------------------------------

@admin_user_routes.route("/view_user_list_by_gender/<string:gender_type>", methods=["GET"])
@admin_token_authentication()
def user_profiles_view_by_gender(current_admin, gender_type):
    return get_user_profiles_by_gender(current_admin, gender_type)