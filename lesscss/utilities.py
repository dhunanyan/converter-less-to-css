import collections
import math
import re
import itertools
from six import string_types


def flatten(lst):
    for element in lst:
        if isinstance(element, collections.abc.Iterable) and not isinstance(element, string_types):
            for sub in flatten(element):
                yield sub
        else:
            yield element


def pairwise(lst):
    if not lst:
        return
    length = len(lst)
    for i in range(length - 1):
        yield lst[i], lst[i + 1]
    yield lst[-1], None


def rename(blocks, scope, stype):
    for p in blocks:
        if isinstance(p, stype):
            p.tokens[0].parse(scope)
            if p.tokens[1]:
                scope.push()
                scope.current = p.tokens[0]
                rename(p.tokens[1], scope, stype)
                scope.pop()


def block_search(block, name):
    if hasattr(block, 'tokens'):
        for b in block.tokens[1]:
            b = b if hasattr(b, 'raw') and b.raw() == name else block_search(b, name)
            if b:
                return b
    return False


def reverse_guard(lst):
    rev = {'<': '>=', '>': '=<', '>=': '<', '=<': '>'}
    return [rev[l] if l in rev else l for l in lst]


def destring(value):
    return value.strip('"\'')


def analyze_number(var, err=''):
    number, unit = split_unit(var)
    if not isinstance(var, string_types):
        return var, unit
    if is_color(var):
        return var, 'color'
    if is_int(number):
        n = int(number)
    elif is_float(number):
        n = float(number)
    else:
        raise SyntaxError('%s `%s`' % (err, var))
    return number, unit


def with_unit(number, unit=None):
    if isinstance(number, tuple):
        number, unit = number
    if number == 0:
        return '0'
    if unit:
        number = str(number)
        if number.startswith('.'):
            number = '0' + number
        return "%s%s" % (number, unit)
    return number if isinstance(number, string_types) else str(number)


def is_color(value):
    if not value or not isinstance(value, string_types):
        return False
    if value[0] == '#' and len(value) in (4, 5, 7, 9):
        try:
            int(value[1:], 16)
            return True
        except ValueError:
            pass
    return False


def is_int(value):
    try:
        int(str(value))
        return True
    except (ValueError, TypeError):
        pass
    return False


def is_variable(value):
    if isinstance(value, string_types):
        return value.startswith('@') or value.startswith('-@')
    elif isinstance(value, tuple):
        value = ''.join(value)
        return value.startswith('@') or value.startswith('-@')
    return False


def is_float(value):
    if not is_int(value):
        try:
            float(str(value))
            return True
        except (ValueError, TypeError):
            pass
    return False


def split_unit(value):
    r = re.search('^(\-?[\d\.]+)(.*)$', str(value))
    return r.groups() if r else ('', '')


def away_from_zero_round(value, ndigits=0):
    p = 10 ** ndigits
    return float(math.floor((value * p) + math.copysign(0.5, value))) / p


def pc_or_float(s):
    if isinstance(s, string_types) and '%' in s:
        return float(s.strip('%')) / 100.0
    return float(s)


def permutations_with_replacement(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in itertools.product(range(n), repeat=r):
        yield list(pool[i] for i in indices)


def convergent_round(value, ndigits=0):
    return round(value, ndigits)