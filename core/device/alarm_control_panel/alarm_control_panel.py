from core.device.entity import Entity
from core.device.hardware import Hardware
from gpiozero import Button
from typing import List
from core.device.alarm_control_panel.zone import Zone, ZoneType
from pydantic import PrivateAttr


class AlarmControlPanel(Entity):
    def __init__(
        self,
        name: str,
        hardware: Hardware = None,
        icon: str = None,
        unique_id: str = None,
        entity_type: str = "alarm_control_panel",
    ):
        Entity.__init__(
            self,
            name=name,
            unique_id=unique_id,
            hardware=hardware,
            entity_type=entity_type,
            icon=icon,
        )
        self.__zones: List[Zone] = []
        self.__callback = disarmed

    def set_zones(self, zones: List[Zone]):
        self.__zones = zones

    def set_alarm(self, alarm):
        self.__callback = alarm

    def state(self):
        state: bool = False
        for zone in self.__zones:
            state = self.__callback(zone)
        return state

def disarmed(zone: Zone):
    return False

def arm_home(zone: Zone):
    if zone.zone_type != ZoneType.MotionSensor:
        return zone.state


def arm_away(zone: Zone):
    return zone.state


def arm_night(zone: Zone):
    if zone.zone_type != ZoneType.MotionSensor:
        return zone.state


def arm_vacation(zone: Zone):
    pass


def arm_custom(zone: Zone):
    pass
