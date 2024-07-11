from flask import Flask, request, jsonify
from flask_cors import CORS
from core.utils.id_generator import generate_id
from core.device_manager import device_manager
from loguru import logger
from core.device.device_factory import DeviceFactory

device_factory = DeviceFactory()
app = Flask(__name__)
CORS(app)


@app.route("/api/device/add", methods=["POST"])
def add_device():
    req = request.get_json()
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
    print(params)
    dev = device_factory.get_device(**params)
    device_manager.add(dev)
    print(dev.model_dump_json(indent=2, exclude_unset=True))
    return "", 200


def normalize_query_param(value):
    return value if len(value) > 1 else value[0]


def normalize_query(params):
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}


@app.route("/api/device/search", methods=["GET"])
def list_device():
    query_params = normalize_query(request.args)
    logger.info(query_params)
    losta = []

    for device in device_manager.list():
        if not query_params:
            losta.append(device.model_dump())
        if query_params.get("name", None) is not None and device.name in query_params["name"]:
            losta.append(device.model_dump())
        if (
            query_params.get("type", None) is not None
            and device.entity_type in query_params["type"]
        ):
            losta.append(device.model_dump())

    response = jsonify(losta)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/device/delete/<device_id>", methods=["DELETE"])
def delete_device(device_id: str):
    device_manager.remove(device_id)
    return "", 200


@app.route("/api/device/update/<device_id>", methods=["PUT"])
def update_device(device_id: str):
    print(device_id)
    return "", 200
