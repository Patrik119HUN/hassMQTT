from core.device.device_builder import DeviceBuilder, device_builder
from core.device.hardware import Hardware
from core.repository import LightRepository
from core.config_manager import config_manager
from class_registry import ClassRegistry

light_registry = ClassRegistry()


@device_builder.register("light")
class LightBuilder(DeviceBuilder):

    __light_repository: LightRepository = None

    def __init__(
        self, light_repository: LightRepository = LightRepository(config_manager["database"])
    ):
        self.__light_repository = light_repository

    def get(self, unique_id: str, name: str, hardware: Hardware, icon: str, **kwargs):
        color_mode = kwargs.get("color_mode", self.__light_repository.get(unique_id)["color_mode"])
        if color_mode not in light_registry:
            raise RuntimeError(f"No such a light type:{color_mode}")
        for x, y in light_registry.items():
            if x == color_mode:
                return y(
                    name=name,
                    unique_id=unique_id,
                    hardware=hardware,
                    icon=icon,
                    entity_type="light",
                )
