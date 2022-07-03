from lesscss import utilities


class Node(object):
    def __init__(self, tokens, lineno=0):
        self.tokens = tokens
        self.lineno = lineno
        self.parsed = False

    def parse(self, scope):
        return self

    def process(self, tokens, scope):
        while True:
            tokens = list(utilities.flatten(tokens))
            done = True
            if any(t for t in tokens if hasattr(t, 'parse')):
                tokens = [
                    t.parse(scope) if hasattr(t, 'parse') else t
                    for t in tokens
                ]
                done = False
            if any(
                    t for t in tokens
                    if (utilities.is_variable(t)) or str(type(t)) ==
                    "<class 'lesscpy.plib.variable.Variable'>"):
                tokens = self.replace_variables(tokens, scope)
                done = False
            if done:
                break
        return tokens

    def replace_variables(self, tokens, scope):
        list = []
        for t in tokens:
            if utilities.is_variable(t):
                list.append(scope.swap(t))
            elif str(type(t)) == "<class 'lesscpy.plib.variable.Variable'>":
                list.append(scope.swap(t.name))
            else:
                list.append(t)
        return list

    def fmt(self, fills):
        raise ValueError('No defined format')