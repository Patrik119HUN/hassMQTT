from typing import List
from core.utils.visitor import Visitor


class CompositeVisitor(Visitor):
    _visitors: List[Visitor] = []

    def add_visitor(self, visitor: Visitor):
        self._visitors.append(visitor)
        return self

    def visit(self, visitable):
        for visitor in self._visitors:
            visitor.visit(visitable)
