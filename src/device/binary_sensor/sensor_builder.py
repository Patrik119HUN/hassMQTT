from src.device.device_builder import DeviceBuilder, device_builder
from src.device.hardware import Hardware
from src.device.binary_sensor import BinarySensor

@device_builder.register("sensor")
class SensorBuilder(DeviceBuilder):
    __sensor_registry = {
        "binary": BinarySensor,
    }

    def get(self, unique_id: str, name: str, hardware: Hardware, icon: str):
        return BinarySensor(name, hardware, icon, unique_id)
