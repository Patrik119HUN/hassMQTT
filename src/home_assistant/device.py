from pydantic import BaseModel, model_validator
from typing import Optional


class Device(BaseModel):
    name: str
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    sw_version: Optional[str] = None
    hw_version: Optional[str] = None
    identifiers: Optional[list[str] | str] = None
    connections: Optional[list[tuple]] = None
    configuration_url: Optional[str] = None
    via_device: Optional[str] = None


class EntityInfo(BaseModel):
    component: str
    """One of the supported MQTT components, for instance `binary_sensor`"""
    """Information about the sensor"""
    device: Optional[Device] = None
    """Information about the device this sensor belongs to"""
    device_class: Optional[str] = None
    """Sets the class of the device, changing the device state and icon that is
        displayed on the frontend."""
    enabled_by_default: Optional[bool] = None
    """Flag which defines if the entity should be enabled when first added."""
    entity_category: Optional[str] = None
    """Classification of a non-primary entity."""
    expire_after: Optional[int] = None
    """If set, it defines the number of seconds after the sensor’s state expires,
        if it’s not updated. After expiry, the sensor’s state becomes unavailable.
            Default the sensors state never expires."""
    force_update: Optional[bool] = None
    """Sends update events even if the value hasn’t changed.\
    Useful if you want to have meaningful value graphs in history."""
    icon: Optional[str] = None
    name: str
    """Name of the sensor inside Home Assistant"""
    object_id: Optional[str] = None
    """Set this to generate the `entity_id` in HA instead of using `name`"""
    qos: Optional[int] = None
    """The maximum QoS level to be used when receiving messages."""
    unique_id: Optional[str] = None
    """Set this to enable editing sensor from the HA ui and to integrate with a
        device"""

    @model_validator
    def device_need_unique_id(cls, values):
        """Check that `unique_id` is set if `device` is provided,\
            otherwise Home Assistant will not link the sensor to the device"""
        device, unique_id = values.get("device"), values.get("unique_id")
        if device is not None and unique_id is None:
            raise ValueError("A unique_id is required if a device is defined")
        return values
