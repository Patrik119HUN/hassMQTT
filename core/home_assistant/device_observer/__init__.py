from .entity_observer import EntityObserver
from .binary_observer import BinaryObserver
from .brightness_observer import BrightnessObserver
from .alarm_observer import AlarmObserver
from .rgb_observer import RGBObserver
from .sensor_observer import SensorObserver

from .observer_factory import ObserverFactory

observer_factory = ObserverFactory()

from core.device.binary_sensor import BinarySensor
from core.device.alarm_control_panel import AlarmControlPanel
from core.home_assistant.device_observer.observer_data import ObserverData
from core.device.light import *

observer_factory.register(BinarySensor, ObserverData(None, SensorObserver, None))
observer_factory.register(BinaryLight, ObserverData(BinaryObserver, None, None))


observer_factory.register(
    BrightnessLight,
    ObserverData(
        BinaryObserver, None, {"brightness_command_topic": BrightnessObserver}
    ),
)

observer_factory.register(
    RGBLight,
    ObserverData(
        BinaryObserver,
        None,
        {
            "rgb_command_topic": RGBObserver,
            "brightness_command_topic": BrightnessObserver,
        },
    ),
)
observer_factory.register(AlarmControlPanel, ObserverData(AlarmObserver, None, None))
