from .discovery_visitor import Discovery
from core.device.entity import Entity
from core.device.binary_sensor import BinarySensor
from core.utils.visitor import Visitor


class SensorVisitor(Discovery, Visitor):
    def visit(self, visitable: Entity):
        if type(visitable) is not BinarySensor:
            return None
        packet = self.packet(visitable)
        packet.pop("command_topic")
        return packet
