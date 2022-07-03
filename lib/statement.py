from .node import Node
from lesscss import utilities


class Statement(Node):
    def parse(self, scope):
        self.parsed = list(utilities.flatten(self.tokens))
        if self.parsed[0] == '@import':
            if len(self.parsed) > 4:
                self.parsed.insert(3, ' ')
        return self

    def fmt(self, fills):
        return ''.join(self.parsed) + fills['eb']