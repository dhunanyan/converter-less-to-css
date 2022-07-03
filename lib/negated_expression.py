from six import string_types

from .node import Node


class NegatedExpression(Node):
    def parse(self, scope):
        val, = self.process(self.tokens, scope)
        if isinstance(val, string_types):
            return '-' + val
        return -val