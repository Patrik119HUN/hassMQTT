from flask import Blueprint, jsonify, request
from core.device_manager import device_manager
from core.device.entity import Entity

list_devices = Blueprint("list_device_servlet", __name__)


@list_devices.route("/list_device", methods=["GET"])
def list_device():
    args = request.args

    def entity_filter(entity: Entity) -> bool:
        if args.get("name", None) is not None and entity.name != args.get("name", None):
            return False
        if args.get("type", None) is not None and entity.entity_type != args.get("type", None):
            return False
        return True

    res = [entity.model_dump() for entity in list(filter(entity_filter, device_manager.list()))]
    response = jsonify(res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
