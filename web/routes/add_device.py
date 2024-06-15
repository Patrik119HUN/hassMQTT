from flask import Blueprint, request
from core.device.device_factory import DeviceFactory
from core.device.hardware import Hardware
from core.utils.id_generator import generate_id
from core.device_manager import device_manager

simple_page = Blueprint("add_device_servlet", __name__)

device_factory = DeviceFactory()


@simple_page.route("/api/device/add", methods=["POST"])
def add_device():
    req = request.get_json()
    print(req)
    params = {
        "unique_id": generate_id(),
        "name": req.get("name"),
        "device_type": req.get("entity_type"),
        "hardware": req.get("hardware"),
        "icon": req.get("icon"),
        "driver": req.get("driver"),
        "address": req.get("address"),
    }
    if req.get("entity_type") == "light":
        params["color_mode"] = req.get("color_mode")

    dev = device_factory.get_device(**params)
    device_manager.add(dev)
    print(dev.model_dump_json(indent=2, exclude_unset=True))
    return "", 200
