from .node import Node


class Import(Node):
    def parse(self, scope):
        if not self.parsed:
            self.parsed = ''.join(self.process(self.tokens, scope))
        return self.parsed

    def fmt(self, fills):
        return ''

    def copy(self):
        return Import([t for t in self.tokens], 0)
