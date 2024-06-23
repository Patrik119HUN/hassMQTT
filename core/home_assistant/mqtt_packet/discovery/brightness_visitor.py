from .discovery_visitor import Discovery
from core.device.entity import Entity
from core.device.light import BrightnessLight
from core.utils.visitor import Visitor


class BrightnessVisitor(Discovery, Visitor):
    def visit(self, visitable: Entity):
        if type(visitable) is not BrightnessLight:
            return None
        packet = self.packet(visitable)
        packet.update(
            {
                "brightness_command_topic": self._subscriber(visitable)
                .add("brightness", "set")
                .build(),
                "brightness_state_topic": self._publisher(visitable)
                .add("brightness", "state")
                .build(),
            }
        )
        return packet
