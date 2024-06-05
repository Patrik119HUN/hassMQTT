from src.device.light import BinaryLight, BrightnessLight, RGBLight
from src.device.binary_sensor import BinarySensor
from src.device.entity import Entity
from loguru import logger


class DeviceFactory:
    __light_registry = {
        "binary": BinaryLight,
        "brightness": BrightnessLight,
        "rgb": RGBLight,
    }
    __sensor_registry = {
        "binary": BinarySensor,
    }

    @classmethod
    def get_device(cls, device_type: str, name: str, unique_id: str, *args, **kwargs) -> Entity:
        created_dev = None
        match device_type:
            case "light":
                created_dev = DeviceFactory.get_light(light_type=kwargs["color_mode"], name=name, unique_id=unique_id)
            case "binary_sensor":
                created_dev = DeviceFactory.get_sensor(kwargs["device_class"], *args, **kwargs)
            case "alarm":
                raise NotImplemented("Alarm not implemented yet")
        logger.debug(f"created an {created_dev.__class__.__name__}")
        return created_dev

    @classmethod
    def get_light(cls, light_type: str, name: str, unique_id: str) -> Entity:
        if light_type not in DeviceFactory.__light_registry:
            raise RuntimeError("No such a light type")
        return DeviceFactory.__light_registry[light_type](name=name, unique_id=unique_id)

    @classmethod
    def get_sensor(cls, sensor_type: str, *args, **kwargs) -> Entity:
        if sensor_type not in DeviceFactory.__sensor_registry:
            raise RuntimeError("No such a sensor type")
        return DeviceFactory.__sensor_registry[sensor_type](*args, **kwargs)
