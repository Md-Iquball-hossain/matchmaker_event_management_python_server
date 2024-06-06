# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint
from app.database import conn
from app.user.services.add_list_service import add_to_short_list, get_favourite_list, add_dislike
from utils.decorator.auth_checker import user_token_authentication
add_list = Blueprint("add_list", __name__)


@add_list.route("/add-favourite", methods=["POST"])
@user_token_authentication()
def add_to_list(current_user):
    return add_to_short_list(current_user)


@add_list.route("/get-favourite-list", methods=["GET"])
@user_token_authentication()
def get_recent_view(current_user):
    return get_favourite_list(current_user)


@add_list.route("/add-dislike", methods=["DELETE"])
@user_token_authentication()
def add_dislike_profile(current_user):
    return add_dislike(current_user)
