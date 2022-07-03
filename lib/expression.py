import operator

from .node import Node
from lesscss import utilities
from lesscss import color


class Expression(Node):
    def parse(self, scope):
        assert (len(self.tokens) == 3)
        expr = self.process(self.tokens, scope)
        A, O, B = [
            e[0] if isinstance(e, tuple) else e for e in expr
            if str(e).strip()
        ]
        try:
            a, ua = utilities.analyze_number(A, 'Illegal element in expression')
            b, ub = utilities.analyze_number(B, 'Illegal element in expression')
        except SyntaxError:
            return ' '.join([str(A), str(O), str(B)])
        if (a is False or b is False):
            return ' '.join([str(A), str(O), str(B)])
        if ua == 'color' or ub == 'color':
            return color.Color().process((A, O, B))
        if a == 0 and O == '/':
            # NOTE(saschpe): The ugliest but valid CSS since sliced bread: 'font: 0/1 a;'
            return ''.join([str(A), str(O), str(B), ' '])
        out = self.operate(a, b, O)
        if isinstance(out, bool):
            return out
        return self.with_units(out, ua, ub)

    def with_units(self, val, ua, ub):
        if not val:
            return str(val)
        if ua or ub:
            if ua and ub:
                if ua == ub:
                    return str(val) + ua
                else:
                    return str(val) + ua
            elif ua:
                return str(val) + ua
            elif ub:
                return str(val) + ub
        return repr(val)

    def operate(self, vala, valb, oper):
        operation = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '=': operator.eq,
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '=<': operator.le,
        }.get(oper)
        if operation is None:
            raise SyntaxError("Unknown operation %s" % oper)
        ret = operation(vala, valb)
        if oper in '+-*/' and int(ret) == ret:
            ret = int(ret)
        return ret

    def expression(self):
        return utilities.flatten(self.tokens)