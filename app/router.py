# Author: Shidul Islam
# Date: 07-11-2023
# */

from flask import Blueprint
from app.auth.routes.auth_user_routes import auth_router
from app.auth.routes.auth_vendor_routes import auth_vendor
from app.user.router import user
from app.vendor.router import vendor
from app.admin.router import admin
from app.external.routes.external_route import external

app_router = Blueprint("app", __name__)

app_router.register_blueprint(auth_router, url_prefix="/auth")
app_router.register_blueprint(auth_vendor, url_prefix="/auth_vendor")   #author: Md. Iquball Hossain(iquball.m360ict@gmail.com)-23.11.23
app_router.register_blueprint(admin, url_prefix="/admin")   #author: Md. Iquball Hossain(iquball.m360ict@gmail.com)-28.11.23
app_router.register_blueprint(user, url_prefix="/user")
app_router.register_blueprint(vendor, url_prefix="/vendor")  #author: Md. Iquball Hossain(iquball.m360ict@gmail.com)-27.11.23
app_router.register_blueprint(external, url_prefix="/external")