from .discovery_visitor import Discovery
from core.utils.visitor import Visitor
from core.device.entity import Entity
from core.device.alarm_control_panel import AlarmControlPanel


class AlarmVisitor(Discovery, Visitor):
    def visit(self, visitable: Entity):
        if type(visitable) is not AlarmControlPanel:
            return None
        packet = self.packet(visitable)
        packet.update(
            {
                "code": '1234'
            }
        )
        return packet 
