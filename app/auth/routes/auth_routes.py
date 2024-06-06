from flask import Blueprint
from app.database import conn
auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/")
def auth_test():
    return "Test auth is running"


@auth_routes.route("/all", methods=["GET"])
def getBooks():
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM auth.user')
    results = cursor.fetchall()

    cursor.close()
    return results
