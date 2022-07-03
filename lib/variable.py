from .node import Node


class Variable(Node):
    def parse(self, scope):
        self.name, _, self.value = self.tokens
        if isinstance(self.name, tuple):
            if len(self.name) > 1:
                self.name, pad = self.name
                self.value.append(pad)
            else:
                self.name = self.name[0]
        scope.add_variable(self)
        return self

    def copy(self):
        return Variable([t for t in self.tokens])

    def fmt(self, fills):
        return ''
