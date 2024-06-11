from src.device.device_builder import DeviceBuilder, device_builder
from src.device.hardware import Hardware
from src.device.alarm_control_panel.alarm_control_panel import AlarmControlPanel


@device_builder.register("alarm")
class AlarmBuilder(DeviceBuilder):

    def get(self, unique_id: str, name: str, hardware: Hardware, icon: str):
        return AlarmControlPanel(name=name, unique_id=unique_id, hardware=hardware, icon=icon)
