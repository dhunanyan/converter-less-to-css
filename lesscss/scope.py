from six import string_types
from . import utilities


class Scope(list):
    def __init__(self, init=False):
        super(Scope, self).__init__()
        self.mixins = {}
        if init:
            self.push()
        self.deferred = False
        self.real = []

    def push(self):
        self.append({
            'variables': {},
            'blocks': [],
            'names': [],
            'current': None
        })

    @property
    def current(self):
        return self[-1]['current']

    @current.setter
    def current(self, value):
        self[-1]['current'] = value

    @property
    def scopename(self):
        return [r['current'] for r in self if r['current']]


    def add_block(self, block):
        self[-1]['blocks'].append(block)
        self[-1]['names'].append(block.raw())

    def remove_block(self, block, index=-1):
        self[index]["blocks"].remove(block)
        self[index]["names"].remove(block.raw())

    def add_mixin(self, mixin):
        raw = mixin.tokens[0][0].raw()
        if raw in self.mixins:
            self.mixins[raw].append(mixin)
        else:
            self.mixins[raw] = [mixin]

    def add_variable(self, variable):
        self[-1]['variables'][variable.name] = variable

    def variables(self, name):
        if isinstance(name, tuple):
            name = name[0]
        if name.startswith('@{'):
            name = '@' + name[2:-1]
        i = len(self)
        while i >= 0:
            i -= 1
            if name in self[i]['variables']:
                return self[i]['variables'][name]
        return False

    def mixins(self, name):
        m = self.search_mixins(name)
        if m:
            return m
        return self.search_mixins(name.replace('?>?', ' '))

    def search_mixins(self, name):
        return self.mixins[name] if name in self.mixins else False

    def blocks(self, name):
        b = self.blocks(name)
        if b:
            return b
        return self.blocks(name.replace('?>?', ' '))

    def search_blocks(self, name):
        i = len(self)
        while i >= 0:
            i -= 1
            if name in self[i]['names']:
                for b in self[i]['blocks']:
                    r = b.raw()
                    if r and r == name:
                        return b
            else:
                for b in self[i]['blocks']:
                    r = b.raw()
                    if r and name.startswith(r):
                        b = utilities.block_search(b, name)
                        if b:
                            return b
        return False

    def update(self, scope, at=0):
        if hasattr(scope, 'mixins') and not at:
            self.mixins.update(scope.mixins)
        self[at]['variables'].update(scope[at]['variables'])
        self[at]['blocks'].extend(scope[at]['blocks'])
        self[at]['names'].extend(scope[at]['names'])

    def swap(self, name):
        if name.startswith('@@'):
            var = self.variables(name[1:])
            if var is False:
                raise SyntaxError('Unknown variable %s' % name)
            name = '@' + utilities.destring(var.value[0])
            var = self.variables(name)
            if var is False:
                raise SyntaxError('Unknown variable %s' % name)
        elif name.startswith('@{'):
            var = self.variables('@' + name[2:-1])
            if var is False:
                raise SyntaxError('Unknown escaped variable %s' % name)
            if isinstance(var.value[0], string_types):
                var.value[0] = utilities.destring(var.value[0])
        else:
            var = self.variables(name)
            if var is False:
                raise SyntaxError('Unknown variable %s' % name)
        return var.value
