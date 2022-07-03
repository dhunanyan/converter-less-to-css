import re
from .node import Node
from lesscss import utilities
from htmlcss import reserved


class Identifier(Node):
    def parse(self, scope):
        names = []
        name = []
        self._subp = ('@media', '@keyframes', '@-moz-keyframes',
                      '@-webkit-keyframes', '@-ms-keyframes')
        if self.tokens and hasattr(self.tokens, 'parse'):
            self.tokens = list(
                utilities.flatten([
                    id.split() + [',']
                    for id in self.tokens.parse(scope).split(',')
                ]))
            self.tokens.pop()
        if self.tokens and any(hasattr(t, 'parse') for t in self.tokens):
            tmp_tokens = []
            for t in self.tokens:
                if hasattr(t, 'parse'):
                    tmp_tokens.append(t.parse(scope))
                else:
                    tmp_tokens.append(t)
            self.tokens = list(utilities.flatten(tmp_tokens))
        if self.tokens and self.tokens[0] in self._subp:
            name = list(utilities.flatten(self.tokens))
            self.subparse = True
        else:
            self.subparse = False
            for n in utilities.flatten(self.tokens):
                if n == '*':
                    name.append('* ')
                elif n in '>+~':
                    if name and name[-1] == ' ':
                        name.pop()
                    name.append('?%s?' % n)
                elif n == ',':
                    names.append(name)
                    name = []
                else:
                    name.append(n)
        names.append(name)
        parsed = self.root(scope, names) if scope else names

        def replace_variables(tokens, scope):
            return [
                scope.swap(t)
                if (utilities.is_variable(t) and not t in reserved.tokens) else t
                for t in tokens
            ]

        parsed = [
            list(utilities.flatten(replace_variables(part, scope)))
            for part in parsed
        ]

        self.parsed = [[
            i for i, j in utilities.pairwise(part)
            if i != ' ' or (j and '?' not in j)
        ] for part in parsed]
        return self

    def root(self, scope, names):
        parent = scope.scopename
        if parent:
            parent = parent[-1]
            if parent.parsed:
                parsed_names = []
                for name in names:
                    ampersand_count = name.count('&')
                    if ampersand_count:
                        filtered_parts = []
                        for part in parent.parsed:
                            if part and part[0] not in self._subp:
                                filtered_parts.append(part)
                        permutations = list(
                            utilities.permutations_with_replacement(
                                filtered_parts, ampersand_count))
                        for permutation in permutations:
                            parsed = []
                            for name_part in name:
                                if name_part == "&":
                                    parent_part = permutation.pop(0)
                                    if parsed and parsed[-1].endswith(']'):
                                        parsed.extend(' ')
                                    if parent_part[-1] == ' ':
                                        parent_part.pop()
                                    parsed.extend(parent_part)
                                else:
                                    parsed.append(name_part)
                            parsed_names.append(parsed)
                    else:
                        for part in parent.parsed:
                            if part and part[0] not in self._subp:
                                parsed = []
                                if name[0] == "@media":
                                    parsed.extend(name)
                                else:
                                    parsed.extend(part)
                                    if part[-1] != ' ':
                                        parsed.append(' ')
                                    parsed.extend(name)
                                parsed_names.append(parsed)
                            else:
                                parsed_names.append(name)
                return parsed_names
        return names

    def raw(self, clean=False):
        if clean:
            return ''.join(''.join(p) for p in self.parsed).replace('?', ' ')
        return '%'.join('%'.join(p) for p in self.parsed).strip().strip('%')

    def copy(self):
        tokens = ([t for t in self.tokens]
                  if isinstance(self.tokens, list) else self.tokens)
        return Identifier(tokens, 0)

    def fmt(self, fills):
        name = ',$$'.join(''.join(p).strip() for p in self.parsed)
        name = re.sub('\?(.)\?', '%(ws)s\\1%(ws)s', name) % fills
        return name.replace('$$', fills['nl']).replace('  ', ' ')