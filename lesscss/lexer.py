import re
import ply.lex as lex
from six import string_types
from .tokens import tokens, significant_ws, literals

from htmlcss import html, css, reserved


class LessLexer:
    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)
        self.lexer.in_property_decl = False
        self.pretok = None
        self.next = None
        self.last = None

    literals = literals
    tokens = tokens
    significant_ws = significant_ws

    states = (
        ('parn', 'inclusive'),
        ('escapequotes', 'inclusive'),
        ('escapeapostrophe', 'inclusive'),
        ('istringquotes', 'inclusive'),
        ('istringapostrophe', 'inclusive'),
        ('iselector', 'inclusive'),
        ('mediaquery', 'inclusive'),
        ('import', 'inclusive'),
    )

    # tokens definition
    def t_css_ident(self, t):
        (r'((\-|\.|\#|\-\-)?'
         '([_a-z]'
         '|[\200-\377]'
         '|\\\[0-9a-f]{1,6}'
         '|\\\[^\s\r\n0-9a-f])'
         '([_a-z0-9\-]'
         '|[\200-\377]'
         '|\\\[0-9a-f]{1,6}'
         '|\\\[^\s\r\n0-9a-f])*)'
         '|\.')
        value = t.value.strip()
        x = value[0]
        if x == '.':
            t.type = 'css_class'
            if t.lexer.lexstate != 'isselector':
                t.lexer.push_state("iselector")
        elif x == '#':
            if len(value) in [4, 7]:
                try:
                    int(value[1:], 16)
                    t.type = 'css_color'
                except ValueError:
                    pass
        elif value == 'when':
            t.type = 'less_when'
        elif value == 'and':
            t.type = 'less_and'
        elif value == 'not':
            t.type = 'less_not'
        elif value in ('from', 'to'):
            t.type = 'css_keyframe_selector'
        elif value in css.tokens:
            t.type = 'css_property'
            t.lexer.in_property_decl = True
        elif (value in html.tokens or value.lower() in html.tokens) and not t.lexer.in_property_decl:
            t.type = 'css_dom'
        elif value.startswith('--'):
            t.type = 'css_user_property'
            t.lexer.in_property_decl = True
        t.value = value
        return t

    t_t_bclose = r'\}'

    t_t_colon = r':'

    t_css_number = r'-?(\d*\.\d+|\d+)(s|%|in|ex|[ecm]m|p[txc]|deg|g?rad|ms?|k?hz|dpi|dpcm|dppx)?'

    t_iselector_less_variable = r'@\{[^@\}]+\}'

    t_iselector_css_class = r'[_a-z0-9\-]+'

    t_mediaquery_t_not = r'not'

    t_mediaquery_t_only = r'only'

    t_mediaquery_t_and = r'and'

    t_mediaquery_t_popen = r'\('
    t_css_color = r'\#[0-9]([0-9a-f]{5}|[0-9a-f]{2})'

    t_parn_css_uri = (
        r'data:[^\)]+'
        '|(([a-z]+://)?'
        '('
        '(/?[\.a-z:]+[\w\.:]*[\\/][\\/]?)+'
        '|([a-z][\w\.\-]+(\.[a-z0-9]+))'
        '(\#[a-z]+)?)'
        ')+'
    )

    t_parn_css_ident = (
        r'(([_a-z]'
        '|[\200-\377]'
        '|\\\[0-9a-f]{1,6}'
        '|\\\[^\r\n\s0-9a-f])'
        '([_a-z0-9\-]|[\200-\377]'
        '|\\\[0-9a-f]{1,6}'
        '|\\\[^\r\n\s0-9a-f])*)'
    )
    t_t_pclose = r'\)'

    t_t_tilde = r'~'

    t_escapequotes_less_variable = r'@\{[^@"\}]+\}'

    t_escapeapostrophe_less_variable = r'@\{[^@\'\}]+\}'

    t_istringapostrophe_less_variable = r'@\{[^@\'\}]+\}'

    t_css_filter = (
        r'\[[^\]]*\]'
        '|(not|lang|nth-[a-z\-]+)\(.+\)'
        '|and[ \t]\([^><=\{]+\)'
    )

    t_istringquotes_less_variable = r'@\{[^@"\}]+\}'

    def t_css_ms_filter(self, t):
        r'(?:progid:|DX\.)[^;\(]*'
        return t

    def t_t_bopen(self, t):
        r'\{'
        t.lexer.in_property_decl = False
        return t

    def t_t_comma(self, t):
        r','
        t.lexer.in_property_decl = False
        return t

    def t_iselector_t_eclose(self, t):
        r'"|\''
        t.lexer.pop_state()
        return t

    def t_iselector_css_filter(self, t):
        (r'\[[^\]]*\]'
         '|(not|lang|nth-[a-z\-]+)\(.+\)'
         '|and[ \t]\([^><\{]+\)')
        return t

    def t_iselector_t_ws(self, t):
        r'[ \t\f\v]+'
        t.lexer.pop_state()
        t.value = ' '
        return t

    def t_iselector_t_bopen(self, t):
        r'\{'
        t.lexer.pop_state()
        return t

    def t_iselector_t_colon(self, t):
        r':'
        t.lexer.pop_state()
        return t

    @lex.TOKEN('|'.join(css.media_features))
    def t_mediaquery_css_media_feature(self, t):
        return t

    def t_mediaquery_t_bopen(self, t):
        r'\{'
        t.lexer.pop_state()
        return t

    def t_mediaquery_t_semicolon(self, t):
        r';'
        t.lexer.pop_state()
        t.lexer.pop_state()
        return t

    def t_import_t_semicolon(self, t):
        r';'
        t.lexer.pop_state()
        return t

    def t_less_variable(self, t):
        r'@@?[\w-]+|@\{[^@\}]+\}'
        v = t.value.lower()
        if v in reserved.tokens:
            t.type = reserved.tokens[v]
            if t.type == "css_media":
                t.lexer.push_state("mediaquery")
            elif t.type == "css_import":
                t.lexer.push_state("import")
        return t

    def t_newline(self, t):
        r'[\n\r]+'
        t.lexer.lineno += t.value.count('\n')

    def t_css_comment(self, t):
        r'(/\*(.|\n|\r)*?\*/)'
        t.lexer.lineno += t.value.count('\n')
        pass

    def t_less_comment(self, t):
        r'//.*'
        pass

    def t_css_important(self, t):
        r'!\s*important'
        t.value = '!important'
        return t

    def t_t_ws(self, t):
        r'[ \t\f\v]+'
        t.value = ' '
        return t

    def t_t_popen(self, t):
        r'\('
        t.lexer.push_state('parn')
        return t

    def t_less_open_format(self, t):
        r'%\('
        t.lexer.push_state('parn')
        return t

    def t_parn_t_pclose(self, t):
        r'\)'
        t.lexer.pop_state()
        return t

    def t_t_semicolon(self, t):
        r';'
        t.lexer.in_property_decl = False
        return t

    def t_t_eopen(self, t):
        r'~"|~\''
        if t.value[1] == '"':
            t.lexer.push_state('escapequotes')
        elif t.value[1] == '\'':
            t.lexer.push_state('escapeapostrophe')
        return t

    def t_escapequotes_t_eclose(self, t):
        r'"'
        t.lexer.pop_state()
        return t

    def t_escapeapostrophe_t_eclose(self, t):
        r'\''
        t.lexer.pop_state()
        return t

    def t_css_string(self, t):
        r'"[^"@]*"|\'[^\'@]*\''
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_t_isopen(self, t):
        r'"|\''
        if t.value[0] == '"':
            t.lexer.push_state('istringquotes')
        elif t.value[0] == '\'':
            t.lexer.push_state('istringapostrophe')
        return t

    def t_istringapostrophe_css_string(self, t):
        r'[^\'@]+'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_istringquotes_css_string(self, t):
        r'[^"@]+'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_istringquotes_t_isclose(self, t):
        r'"'
        t.lexer.pop_state()
        return t

    def t_istringapostrophe_t_isclose(self, t):
        r'\''
        t.lexer.pop_state()
        return t

    def t_error(self, t):
        raise SyntaxError(
            "Illegal character '%s' line %d" % (t.value[0], t.lexer.lineno))
        t.lexer.skip(1)

    def file(self, filename):
        with open(filename) as f:
            self.lexer.input(f.read())
        return self

    def input(self, f):
        if isinstance(f, string_types):
            with open(f) as f:
                self.lexer.input(f.read())
        else:
            self.lexer.input(f.read())

    def token(self):
        if self.next:
            t = self.next
            self.next = None
            return t
        while True:
            t = self.lexer.token()
            if not t:
                return t
            if t.type == 't_ws' and (
                    self.pretok or
                    (self.last and self.last.type not in self.significant_ws)):
                continue
            self.pretok = False
            if t.type == 't_bclose' and self.last and \
                    self.last.type not in ('t_bopen', 't_bclose') and \
                    self.last.type != 't_semicolon' and not (hasattr(t, 'lexer') and
                                                             (
                                                                     t.lexer.lexstate == 'escapequotes' or t.lexer.lexstate == 'escapeapostrophe')):
                self.next = t
                token = lex.LexToken()
                token.type = 't_semicolon'
                token.value = ';'
                token.lineno = t.lineno
                token.lexpos = t.lexpos
                self.last = token
                self.lexer.in_property_decl = False
                return token
            self.last = t
            break
        return t
