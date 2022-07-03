import re
import math
try:
    from urllib.parse import quote as urlquote
except ImportError:
    from urllib import quote as urlquote
from six import string_types
from .node import Node
from lesscss import utilities
import lesscss.color as Color
from htmlcss.colors import cssColors


class Call(Node):
    def parse(self, scope):
        name = ''.join(self.tokens[0])
        parsed = self.process(self.tokens[1:], scope)

        if name == '%(':
            name = 'sformat'
        elif name in ('~', 'e'):
            name = 'escape'
        color = Color.Color()
        args = [
            t for t in parsed
            if not isinstance(t, string_types) or t not in '(),'
        ]
        if hasattr(self, name):
            try:
                return getattr(self, name)(*args)
            except ValueError:
                pass

        if hasattr(color, name):
            try:
                result = getattr(color, name)(*args)
                try:
                    return result + ' '
                except TypeError:
                    return result
            except ValueError:
                pass
        return name + ''.join([p for p in parsed])

    def escape(self, string, *args):
        return utilities.destring(string.strip('~'))

    def sformat(self, string, *args):
        format = string
        items = []
        m = re.findall('(%[asdA])', format)
        if m and not args:
            raise SyntaxError('Not enough arguments...')
        i = 0
        for n in m:
            v = {
                '%A': urlquote,
                '%s': utilities.destring,
            }.get(n, str)(args[i])
            items.append(v)
            i += 1
        format = format.replace('%A', '%s')
        format = format.replace('%d', '%s')
        return format % tuple(items)

    def isnumber(self, string, *args):
        try:
            n, u = utilities.analyze_number(string)
        except SyntaxError:
            return False
        return True

    def iscolor(self, string, *args):
        return string in cssColors

    def isurl(self, string, *args):
        arg = utilities.destring(string)
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            # localhost...
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            # optional port
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE)
        return regex.match(arg)

    def isstring(self, string, *args):
        regex = re.compile(r'\'[^\']*\'|"[^"]*"')
        return regex.match(string)

    def iskeyword(self, string, *args):
        return string in ('when', 'and', 'not')

    def increment(self, value, *args):
        n, u = utilities.analyze_number(value)
        return utilities.with_unit(n + 1, u)

    def decrement(self, value, *args):
        n, u = utilities.analyze_number(value)
        return utilities.with_unit(n - 1, u)

    def add(self, *args):
        if len(args) <= 1:
            return 0
        return sum([int(v) for v in args])

    def round(self, value, *args):
        n, u = utilities.analyze_number(value)
        return utilities.with_unit(
            int(utilities.away_from_zero_round(float(n))), u)

    def ceil(self, value, *args):
        n, u = utilities.analyze_number(value)
        return utilities.with_unit(int(math.ceil(n)), u)

    def floor(self, value, *args):
        n, u = utilities.analyze_number(value)
        return utilities.with_unit(int(math.floor(n)), u)

    def percentage(self, value, *args):
        n, u = utilities.analyze_number(value)
        n = int(n * 100.0)
        u = '%'
        return utilities.with_unit(n, u)