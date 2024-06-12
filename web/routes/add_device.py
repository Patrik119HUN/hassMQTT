from flask import Blueprint, request

simple_page = Blueprint("add_device_servlet", __name__)


@simple_page.route("/add_device", methods=["POST"])
def add_device():
    req = request.get_json()
    return "", 200
