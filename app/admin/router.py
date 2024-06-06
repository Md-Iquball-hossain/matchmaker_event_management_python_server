
#---------------------------------- Topics : Admin router, Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------------------------

from flask import Blueprint
from app.admin.vendor_admin.routes.admin_create_notice_for_vendor_routes import admin_create_notice_for_vendor_routes
from app.admin.vendor_admin.routes.admin_view_vendor_all_notice_list_routes import admin_vendor_all_notice_list_routes
from app.admin.vendor_admin.routes.admin_view_vendor_profile_list_routes import admin_vendor_profile_list_routes
from app.admin.vendor_admin.routes.admin_delete_vendor_profile_routes import admin_delete_vendor_profile_routes
from app.admin.vendor_admin.routes.admin_view_vendor_helpdesk_msg_routes import admin_vendor_helpdesk_message_routes
from app.admin.admin_profile.admin_profile_routes.admin_profile_routes import admin_profile
from app.admin.user_admin.routes.user_routes import admin_user_routes
from app.admin.vendor_admin.routes.vendor_service_routes import admin_vendor_service
admin = Blueprint("admin", __name__)

admin.register_blueprint(admin_user_routes, url_prefix="/" )
admin.register_blueprint(admin_profile, url_prefix="/")
admin.register_blueprint(admin_create_notice_for_vendor_routes, url_prefix="/")
admin.register_blueprint(admin_vendor_profile_list_routes, url_prefix="/")
admin.register_blueprint(admin_delete_vendor_profile_routes, url_prefix="/")
admin.register_blueprint(admin_vendor_helpdesk_message_routes, url_prefix="/")
admin.register_blueprint(admin_vendor_all_notice_list_routes, url_prefix="/")
admin.register_blueprint(admin_vendor_service, url_prefix="/")
