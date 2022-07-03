<h1 align="center">  Kompilator Less.js do CSS </h1>

## Spis treści

- [Spis treści](#spis-treści)
- [Informacje o projekcie <a name="doc_scube"></a>](#informacje-o-projekcie-)
- [Spis tokenów <a name="description"></a>](#spis-tokenów-)
  - [SEPARATORS](#separators)

  1. [Graficzny interfejs użytkownika](#gui)

  2. [Terminal](#cl)

- [Testy](#tests)

  1. [Prawidłowy kod](#pk)

  2. [Nieprawidłowy kod](#nk)

- [Możliwości rozbudowy programu](#extend)

## Informacje o projekcie <a name="doc_scube"></a>

Autorzy: <br>

- Maciej Ciepał `maciejciepal@student.agh.edu.pl`
- Davit Hunanyan `hunanyan@student.agh.edu.pl`

Główne cele i założenia projektu: <br>

- Translacja kodu z Less.js do CSS

Język implementacji: Python <br>

Generator parserów: ANTLR4 <br><br>
Narzędzie ANTLR zostało użyte do realizacji projektu. Lekser oraz generator parsera wchodzą w jego skład.

Jak ma wyglądać schemat projektu:<br>
`Lexer -> Parser -> Listener`

## Spis tokenów <a name="description"></a>

### SEPARATORS

````
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_BlockStart = r'\{'
t_BlockEnd = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_GT = r'>'
t_LT = r'<'
t_TIL = r'~'
t_COLOR = r':'
t_SEMI = r';'
t_COMMA = r','
t_DOT = r'\.'
t_DOLLAR = r'\$'
t_AT = r'@'
t_PARENTREF = r'&'
t_HASH = r'#'
t_COLONCOLON = r'::'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_DIV = r'\/'
t_MINUS = r'-'
t_PERC = r'%'
t_EQEQ = r'=='
t_GTEQ = r'>='
t_LTEQ = r'<='
t_NOTEQ = r'!='
t_EQ = r'='
t_PIPE_EQ = r'\|='
t_TILD_EQ = r'~='
```css
