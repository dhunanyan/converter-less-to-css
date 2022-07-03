from .node import Node
from lesscss import utilities
from lib.identifier import Identifier


class Block(Node):
    def parse(self, scope):
        if not self.parsed:
            scope.push()
            self.name, inner = self.tokens
            scope.current = self.name
            scope.real.append(self.name)
            if not self.name.parsed:
                self.name.parse(scope)
            if not inner:
                inner = []
            inner = list(utilities.flatten([p.parse(scope) for p in inner if p]))
            self.parsed = []
            self.inner = []
            inner_media_queries = []
            sibling_media_queries = []
            for p in inner:
                if not isinstance(p, Block):
                    self.parsed.append(p)
                elif p.tokens[1] is not None and p.name.tokens[0] == '@media':
                    inner_media_queries.append(p)
                else:
                    self.inner.append(p)
            for mb in inner_media_queries:
                if self.name.tokens[0] == '@media':
                    part_a = self.name.tokens[2:][0][0][0]
                    part_b = mb.name.tokens[2:][0]
                    cond = [
                        '@media', ' ', [
                            part_a, (' ', 'and', ' '),
                            part_b
                        ]
                    ]
                    mb = Block([Identifier(cond), mb.parsed + mb.inner]).parse(scope)
                    sibling_media_queries += mb
                    for block in mb:
                        scope.add_block(block)
                else:
                    cbs = Block([self.tokens[0], mb.parsed + mb.inner]).parse(scope)
                    for cb in cbs:
                        new_mb = Block([mb.tokens[0], [cb]]).parse(scope)
                        sibling_media_queries += new_mb
                        for block in new_mb:
                            scope.add_block(block)
            scope.real.pop()
            scope.pop()
            if self.inner or self.parsed:
                return [self] + sibling_media_queries
            else:
                return sibling_media_queries
        else:
            return [self]

    def raw(self, clean=False):
        try:
            return self.tokens[0].raw(clean)
        except (AttributeError, TypeError):
            pass

    def fmt(self, fills):
        f = "%(identifier)s%(ws)s{%(nl)s%(proplist)s}%(eb)s"
        out = []
        name = self.name.fmt(fills)
        if self.parsed and any(
                p for p in self.parsed
                if str(type(p)) != "<class 'lesscpy.plib.variable.Variable'>"):
            fills.update({
                'identifier':
                name,
                'proplist':
                ''.join([p.fmt(fills) for p in self.parsed if p]),
            })
            out.append(f % fills)
        if hasattr(self, 'inner'):
            if self.name.subparse and len(self.inner) > 0:  # @media
                inner = ''.join([p.fmt(fills) for p in self.inner])
                inner = inner.replace(fills['nl'],
                                      fills['nl'] + fills['tab']).rstrip(
                                          fills['tab'])
                if not fills['nl']:
                    inner = inner.strip()
                fills.update({
                    'identifier': name,
                    'proplist': fills['tab'] + inner
                })
                out.append(f % fills)
            else:
                out.append(''.join([p.fmt(fills) for p in self.inner]))
        return ''.join(out)

    def copy(self):
        name, inner = self.tokens
        if inner:
            inner = [u.copy() if u else u for u in inner]
        if name:
            name = name.copy()
        return Block([name, inner], 0)

    def copy_inner(self, scope):
        if self.tokens[1]:
            tokens = [u.copy() if u else u for u in self.tokens[1]]
            out = [p for p in tokens if p]
            utility.rename(out, scope, Block)
            return out
        return None