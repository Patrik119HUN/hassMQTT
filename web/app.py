from flask import Flask, request, jsonify
from flask_cors import CORS
from core.utils.id_generator import generate_id
from core.device_manager import device_manager
from loguru import logger
from core.device.entity import Entity
from core.repository import AlarmRepository, LightRepository, SensorRepository
from core.device.driver import DriverFactory
from core.device.entity import Hardware
from attrs import asdict, has

app = Flask(__name__)
CORS(app)


@app.route("/api/device/add", methods=["POST"])
def add_device():
    req = request.get_json()
    entity_params = {
        "name": req.get("name"),
        "unique_id": generate_id(),
        "entity_type": req.get("entity_type"),
        "icon": req.get("icon"),
    }
    entity = Entity(**entity_params)
    entity.hardware = Hardware(**req.get("hardware"))
    driver = DriverFactory.get(driver=req.get("driver"), address=req.get("address"))
    if req.get("entity_type") == "light":
        LightRepository.create_light(entity, req.get("color_mode"), driver)
    # device_manager.add(entity)
    return "", 200


def normalize_query_param(value):
    return value if len(value) > 1 else value[0]


def normalize_query(params):
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}


import json
from core.device.driver.abstract_driver import AbstractDriver


def custom_asdict(obj):
    def convert_value(value):
        if isinstance(value, AbstractDriver):
            return str(value.__class__.__name__)
        else:
            return value

    return {
        k: convert_value(v)
        for k, v in asdict(
            obj, recurse=False, filter=lambda attr, _: not attr.name.startswith("_")
        ).items()
    }


@app.route("/api/device/search", methods=["GET"])
def list_device():
    query_params = normalize_query(request.args)
    logger.info(query_params)
    losta = []

    for device in device_manager.list():
        if not query_params:
            losta.append(custom_asdict(device))
        if (
            query_params.get("name", None) is not None
            and device.name in query_params["name"]
        ):
            losta.append(custom_asdict(device))
        if (
            query_params.get("type", None) is not None
            and device.entity_type in query_params["type"]
        ):
            losta.append(custom_asdict(device))
    response = jsonify(losta)
    return response


@app.route("/api/device/delete/<device_id>", methods=["DELETE"])
def delete_device(device_id: str):
    device_manager.remove(device_id)
    return "", 200


@app.route("/api/device/update/<device_id>", methods=["PUT"])
def update_device(device_id: str):
    print(device_id)
    return "", 200


if __name__ == "__main__":
    app.run()
