from .discovery_visitor import Discovery
from core.device.entity import Entity
from core.device.light import RGBLight
from core.utils.visitor import Visitor


class RGBVisitor(Discovery, Visitor):
    def visit(self, visitable: Entity):
        if type(visitable) is not RGBLight:
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
                "rgb_state_topic": self._subscriber(visitable).add("rgb", "state").build(),
                "rgb_command_topic": self._publisher(visitable).add("rgb", "set").build(),
            }
        )
        return packet
