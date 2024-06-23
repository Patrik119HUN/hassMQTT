from .discovery_visitor import Discovery
from core.device.entity import Entity
from core.device.light import BinaryLight
from core.utils.visitor import Visitor


class BinaryVisitor(Discovery, Visitor):
    def visit(self, visitable: Entity):
        if type(visitable) is not BinaryLight:
            return None
        return self.packet(visitable)
