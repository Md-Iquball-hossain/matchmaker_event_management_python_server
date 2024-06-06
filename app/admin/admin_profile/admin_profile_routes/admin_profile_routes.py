#---------------------------------- Topics : Admin profile all API routes, Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

from flask import Blueprint
from app.admin.admin_profile.admin_profile_service.admin_profile_service import create_admin_profile, login_admin, view_admin_profile_list , get_single_admin_profiles, superadmin_get_specific_admin_profile,update_specific_admin, update_admin_personal_profile, delete_admin_profile, view_admin_profiles_by_status
from utils.decorator.auth_checker import admin_token_authentication

admin_profile = Blueprint("admin_profile", __name__)

#---------------------------------- Topics : Login Admin profile endpoint , Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

@admin_profile.route("/admin_profile_login", methods=["POST"])
def admin_login():
    return login_admin()

#---------------------------------- Topics : Admin profile create API endpoint , Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

@admin_profile.route("/create_admin_profile", methods=["POST"])
@admin_token_authentication()
def admin_create(current_admin):
    return create_admin_profile(current_admin)

#---------------------------------- Topics : All Admin profile list view profile endpoint , Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

@admin_profile.route("/view_admin_profile_list", methods=["GET"])
@admin_token_authentication()
def superadmin_view_all_profile(current_admin):
    return view_admin_profile_list(current_admin)

#---------------------------------- Topics : Login Admin profile endpoint , Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

@admin_profile.route("/view_admin_single_profile", methods=["GET"])
@admin_token_authentication()
def admin_all_profile_view(current_admin):
    return get_single_admin_profiles(current_admin)

#---------------------------------- Topics : SuperAdmin View specific Admin profile endpoint , Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

@admin_profile.route("/superadmin_get_specific_admin_profile/<int:admin_id>", methods=["GET"])
@admin_token_authentication()
def admin_specific_profile_view(current_admin,admin_id):
    return superadmin_get_specific_admin_profile(current_admin,admin_id)

#---------------------------------- Topics : Update specific Admin profile endpoint , Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

@admin_profile.route("/edit_specific_admin_profile/<int:admin_id>", methods=["PUT"])
@admin_token_authentication()
def admin_single_profile_edit(current_admin,admin_id):
    return update_specific_admin(current_admin,admin_id) 

#---------------------------------- Topics : Update personal Admin profile endpoint , Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

@admin_profile.route("/edit_personal_admin_profile", methods=["PUT"])
@admin_token_authentication()
def edit_admin_personal_profile(current_admin):
    return update_admin_personal_profile(current_admin) 

#---------------------------------- Topics : Delete Specific Admin profile endpoint , Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

@admin_profile.route("/delete_specific_admin_profile/<int:admin_id>", methods=["DELETE"])
@admin_token_authentication()
def delete_admins_profile(current_admin,admin_id):
    return delete_admin_profile(current_admin,admin_id) 

#----------- Topics : Admin view personal profile list using profile status , Author: Md. Iquball Hossain, Date: 12-12-2023 ---------------

@admin_profile.route("/admin_profile_view_as_status/<string:status>", methods=["GET"])
@admin_token_authentication()
def view_admin_profile_by_status(current_admin, status):
    return view_admin_profiles_by_status(current_admin,status) 