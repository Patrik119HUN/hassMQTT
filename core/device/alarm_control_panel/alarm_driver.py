from typing import List
from abc import ABC, abstractmethod
from .zone import Zone, ZoneType
import threading
import time

class AlarmState(ABC):
    _event = threading.Event()

    @abstractmethod
    def handle_request(self, zones: List[Zone]):
        pass


class HomeState(AlarmState):
    """
    It does not check the motion sensors and it has a timeout to turn of the alarm
    """

    def __init__(self):
        #threading.Thread(target=self.state).start()
        pass
    
    def state(self):
        print("triggered")

    def handle_request(self, zones: List[Zone]):
        for zone in zones:
            if zone.zone_type != ZoneType.MotionSensor:
                if zone.state:
                    self.state()
                    time.sleep(1)


class AwayState(AlarmState):
    """
    It checks the motion sensors and it has a timeout to turn of the alarm
    """

    def handle_request(self, zones: List[Zone]):
        for zone in zones:
            if zone.state:
                print("triggered")


class NightState(AlarmState):
    """
    It does not check the motion sensors and it has a NO timeout to turn of the alarm
    """

    def handle_request(self, zones: List[Zone]):
        for zone in zones:
            if zone.zone_type != ZoneType.MotionSensor:
                if zone.state:
                    print("triggered")


class AlarmDriver:
    __zones: List[Zone] = []
    __state: AlarmState = None

    def __init__(self):
        pass

    def set_state(self, state: AlarmState):
        self.__state = state

    def request(self):
        self.__state.handle_request()
