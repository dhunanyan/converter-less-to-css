from .node import Node


class Deferred(Node):
    def __init__(self, mixin, args, lineno=0):
        self.tokens = [mixin, args]
        self.lineno = lineno

    def parse(self, scope, error=False, depth=0):
        res = False
        ident, args = self.tokens
        ident.parse(scope)
        mixins = scope.mixins(ident.raw())

        if not mixins:
            ident.parse(None)
            mixins = scope.mixins(ident.raw())

        if depth > 64:
            raise SyntaxError('NameError `%s`' % ident.raw(True))

        if not mixins:
            if scope.deferred:
                store = [t for t in scope.deferred.parsed[-1]]
                i = 0
                while scope.deferred.parsed[-1]:
                    scope.current = scope.deferred
                    ident.parse(scope)
                    mixins = scope.mixins(ident.raw())
                    scope.current = None
                    if mixins or i > 64:
                        break
                    scope.deferred.parsed[-1].pop()
                    i += 1
                scope.deferred.parsed[-1] = store

        if not mixins:
            block = scope.blocks(ident.raw())
            if not block:
                ident.parse(None)
                block = scope.blocks(ident.raw())
            if block:
                scope.current = scope.real[-1] if scope.real else None
                res = block.copy_inner(scope)
                scope.current = None

        if mixins:
            for mixin in mixins:
                scope.current = scope.real[-1] if scope.real else None
                res = mixin.call(scope, args)
                if res:
                    [scope.add_variable(v) for v in mixin.vars]
                    scope.deferred = ident
                    break

        if res:
            store = [t for t in scope.deferred.parsed[-1]
                     ] if scope.deferred else False
            tmp_res = []
            for p in res:
                if p:
                    if isinstance(p, Deferred):
                        tmp_res.append(p.parse(scope, depth=depth + 1))
                    else:
                        tmp_res.append(p.parse(scope))
            res = tmp_res
            while (any(t for t in res if isinstance(t, Deferred))):
                res = [p.parse(scope) for p in res if p]
            if store:
                scope.deferred.parsed[-1] = store

        if error and not res:
            raise SyntaxError('NameError `%s`' % ident.raw(True))
        return res

    def copy(self):
        return self