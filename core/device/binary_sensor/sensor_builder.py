from core.device.device_builder import DeviceBuilder, device_builder
from core.device.hardware import Hardware
from core.device.binary_sensor import BinarySensor

@device_builder.register("sensor")
class SensorBuilder(DeviceBuilder):
    def get(self, unique_id: str, name: str, hardware: Hardware, icon: str):
        return BinarySensor(name, hardware, icon, unique_id)
