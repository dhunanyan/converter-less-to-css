from .node import Node


class KeyframeSelector(Node):
    def parse(self, scope):
        self.keyframe, = [
            e[0] if isinstance(e, tuple) else e for e in self.tokens
            if str(e).strip()
        ]
        self.subparse = False
        return self

    def copy(self):
        return KeyframeSelector(self.tokens, 0)

    def fmt(self, fills):
        return self.keyframe
