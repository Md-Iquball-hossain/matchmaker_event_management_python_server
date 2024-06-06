# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint
from app.database import conn
from app.user.services.my_matches_service import my_matches_list, todays_matches_list, my_matches_single_preference, my_matches_single_list_preference, near_me_list
from utils.decorator.auth_checker import user_token_authentication
my_matches = Blueprint("matches", __name__)


@my_matches.route("/my-matches", methods=["GET"])
@user_token_authentication()
def my_match(current_user):
    return my_matches_list(current_user)


@my_matches.route("/my-matches/<int:id>", methods=["GET"])
@user_token_authentication()
def my_match_single(current_user, id):
    return my_matches_single_preference(current_user, id)


@my_matches.route("/my-matches/<int:id>", methods=["GET"])
@user_token_authentication()
def my_match_single_list(current_user, id):
    return my_matches_single_list_preference(current_user, id)


@my_matches.route("/todays-matches", methods=["GET"])
@user_token_authentication()
def recent_match(current_user):
    return todays_matches_list(current_user)


@my_matches.route("/near-me", methods=["GET"])
@user_token_authentication()
def near_me(current_user):
    return near_me_list(current_user)
