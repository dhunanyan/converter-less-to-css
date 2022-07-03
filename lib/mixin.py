import sys
import copy
import itertools
from .node import Node
from .block import Block
from .expression import Expression
from .variable import Variable
from lesscss import utilities


class Mixin(Node):
    def parse(self, scope):
        self.name, args, self.guards = self.tokens[0]
        self.args = [a for a in utilities.flatten(args) if a]
        self.body = Block([None, self.tokens[1]], 0)
        self.vars = list(
            utilities.flatten([
                list(v.values()) for v in [s['__variables__'] for s in scope]
            ]))
        return self

    def raw(self):
        return self.name.raw()

    def parse_args(self, args, scope):
        arguments = list(zip(args,
                             [' '] * len(args))) if args and args[0] else None
        zl = itertools.zip_longest if sys.version_info[
            0] == 3 else itertools.izip_longest
        if self.args:
            parsed = [
                v if hasattr(v, 'parse') else v for v in copy.copy(self.args)
            ]
            args = args if isinstance(args, list) else [args]
            vars = [
                self._parse_arg(var, arg, scope)
                for arg, var in zl([a for a in args], parsed)
            ]
            for var in vars:
                if var:
                    var.parse(scope)
            if not arguments:
                arguments = [v.value for v in vars if v]
        if not arguments:
            arguments = ''
        Variable(['@arguments', None, arguments]).parse(scope)

    def _parse_arg(self, var, arg, scope):
        if isinstance(var, Variable):
            if arg:
                if utilities.is_variable(arg[0]):
                    tmp = scope.variables(arg[0])
                    if not tmp:
                        return None
                    val = tmp.value
                else:
                    val = arg
                var = Variable(var.tokens[:-1] + [val])
        else:
            if utilities.is_variable(var):
                if arg is None:
                    raise SyntaxError('Missing argument to mixin')
                elif utilities.is_variable(arg[0]):
                    tmp = scope.variables(arg[0])
                    if not tmp:
                        return None
                    val = tmp.value
                else:
                    val = arg
                var = Variable([var, None, val])
            else:
                return None
        return var

    def parse_guards(self, scope):
        if self.guards:
            cor = True if ',' in self.guards else False
            for g in self.guards:
                if isinstance(g, list):
                    res = (g[0].parse(scope)
                           if len(g) == 1 else Expression(g).parse(scope))
                    if cor:
                        if res:
                            return True
                    elif not res:
                        return False
        return True

    def call(self, scope, args=[]):
        ret = False
        if args:
            args = [[
                a.parse(scope) if isinstance(a, Expression) else a for a in arg
            ] if arg else arg for arg in args]
        try:
            self.parse_args(args, scope)
        except SyntaxError:
            pass
        else:
            if self.parse_guards(scope):
                body = self.body.copy()
                ret = body.tokens[1]
                if ret:
                    utilities.rename(ret, scope, Block)
        return ret