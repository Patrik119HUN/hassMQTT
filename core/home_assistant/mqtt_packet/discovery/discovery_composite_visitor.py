from core.utils.composite_visitor import CompositeVisitor
from typing import Dict


class DiscoveryCompositeVisitor(CompositeVisitor):
    _packet: Dict[str, str]

    def visit(self, visitable):
        for visitor in self._visitors:
            ret = visitor.visit(visitable)
            if ret is not None:
                self._packet = ret

    def get(self):
        return self._packet
