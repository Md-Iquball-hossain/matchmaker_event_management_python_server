#----------------------------------  Topics : vendor profile router, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

from flask import Blueprint
from app.vendor.routes.vendor_profile_routes import vendor_profile_routes
from app.vendor.routes.vendor_notice_view_routes import vendor_notice_view_routes
from app.vendor.routes.vendor_helpdesk_routes import vendor_helpdesk_message
from app.vendor.routes.vendor_service_routes import vendor_service_routes

vendor = Blueprint("vendor", __name__)

vendor.register_blueprint(vendor_profile_routes, url_prefix="/")
vendor.register_blueprint(vendor_notice_view_routes, url_prefix="/")
vendor.register_blueprint(vendor_helpdesk_message, url_prefix="/")
vendor.register_blueprint(vendor_service_routes, url_prefix="/")
