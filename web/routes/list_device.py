from flask import Blueprint, jsonify, request
from core.device_manager import device_manager
from core.device.entity import Entity
from typing import List, Any
from loguru import logger

list_devices = Blueprint("list_device_servlet", __name__)


def normalize_query_param(value):
    """
    Given a non-flattened query parameter value,
    and if the value is a list only containing 1 item,
    then the value is flattened.

    :param value: a value from a query parameter
    :return: a normalized query parameter value
    """
    return value if len(value) > 1 else value[0]


def normalize_query(params):
    """
    Converts query parameters from only containing one value for each parameter,
    to include parameters with multiple values as lists.

    :param params: a flask query parameters data structure
    :return: a dict of normalized query parameters
    """
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}


@list_devices.route("/api/device/search", methods=["GET"])
def list_device():
    query_params = normalize_query(request.args)
    logger.info(query_params)
    losta = []

    for device in device_manager.list():
        if not query_params:
            losta.append(device.model_dump())
        if query_params.get("name", None) is not None and device.name in query_params["name"]:
            losta.append(device.model_dump())
        if query_params.get("type", None) is not None and device.entity_type in query_params["type"]:
            losta.append(device.model_dump())

    response = jsonify(losta)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
