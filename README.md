<h1 align="center">  Kompilator Less.js do CSS </h1>

## Spis treści

- [Spis treści](#spis-treści)
- [Informacje o projekcie <a name="doc_scube"></a>](#informacje-o-projekcie-)
- [Spis tokenów <a name="description"></a>](#spis-tokenów-)
  - [Separatory](#separatory)
  - [URL-e](#url-e)
  - [Opcje Import-u](#opcje-import-u)
  - [Misc Funkcje](#misc-funkcje)
  - [String-i](#string-i)
  - [Listy](#listy)
  - [Matematyczne Funkcje](#matematyczne-funkcje)
  - [Typy](#typy)
  - [Funkcje Kolorów](#funkcje-kolorów)
  - [Kanały Kolorów](#kanały-kolorów)
  - [Operacje na Kolorach](#operacje-na-kolorach)
  - [Blendowanie Kolorów](#blendowanie-kolorów)
  - [Łączniki](#łączniki)
  - [Literały Stringów](#literały-stringów)
  - [Linia Stringu](#linia-stringu)
  - [Wieloliniowy String](#wieloliniowy-string)
  - [Pusta Przestrzeń](#pusta-przestrzeń)
  - [Nulle I Tym Podobne](#nulle-i-tym-podobne)

  - [Separatory](#separatory)
  - [URL-e](#url-e)
  - [Opcje Import-u](#opcje-import-u)
  - [Misc Funkcje](#misc-funkcje)
  - [String-i](#string-i)
  - [Listy](#listy)
  - [Matematyczne Funkcje](#matematyczne-funkcje)
  - [Typy](#typy)
  - [Funkcje Kolorów](#funkcje-kolorów)
  - [Kanały Kolorów](#kanały-kolorów)
  - [Operacje na Kolorach](#operacje-na-kolorach)
  - [Blendowanie Kolorów](#blendowanie-kolorów)
  - [Łączniki](#łączniki)
  - [Literały Stringów](#literały-stringów)
  - [Linia Stringu](#linia-stringu)
  - [Wieloliniowy String](#wieloliniowy-string)
  - [Pusta Przestrzeń](#pusta-przestrzeń)
  - [Nulle I Tym Podobne](#nulle-i-tym-podobne)

  - [Separatory](#separatory)
  - [URL-e](#url-e)
  - [Opcje Import-u](#opcje-import-u)
  - [Misc Funkcje](#misc-funkcje)
  - [String-i](#string-i)
  - [Listy](#listy)
  - [Matematyczne Funkcje](#matematyczne-funkcje)
  - [Typy](#typy)
  - [Funkcje Kolorów](#funkcje-kolorów)
  - [Kanały Kolorów](#kanały-kolorów)
  - [Operacje na Kolorach](#operacje-na-kolorach)
  - [Blendowanie Kolorów](#blendowanie-kolorów)
  - [Łączniki](#łączniki)
  - [Literały Stringów](#literały-stringów)
  - [Linia Stringu](#linia-stringu)
  - [Wieloliniowy String](#wieloliniowy-string)
  - [Pusta Przestrzeń](#pusta-przestrzeń)

  - [Separatory](#separatory)
  - [URL-e](#url-e)
  - [Opcje Import-u](#opcje-import-u)
  - [Misc Funkcje](#misc-funkcje)
  - [String-i](#string-i)
  - [Listy](#listy)
  - [Matematyczne Funkcje](#matematyczne-funkcje)
  - [Typy](#typy)
  - [Funkcje Kolorów](#funkcje-kolorów)
  - [Kanały Kolorów](#kanały-kolorów)
  - [Operacje na Kolorach](#operacje-na-kolorach)
  - [Blendowanie Kolorów](#blendowanie-kolorów)
  - [Literały Stringów](#literały-stringów)
  - [Linia Stringu](#linia-stringu)
  - [Wieloliniowy String](#wieloliniowy-string)
  - [Pusta Przestrzeń](#pusta-przestrzeń)

  - [Separatory](#separatory)
  - [URL-e](#url-e)
  - [Opcje Import-u](#opcje-import-u)
  - [Misc Funkcje](#misc-funkcje)
  - [String-i](#string-i)
  - [Listy](#listy)
  - [Matematyczne Funkcje](#matematyczne-funkcje)
  - [Typy](#typy)
  - [Funkcje Kolorów](#funkcje-kolorów)
  - [Kanały Kolorów](#kanały-kolorów)
  - [Operacje na Kolorach](#operacje-na-kolorach)
  - [Typy](#typy-1)

  - [Separatory](#separatory)
  - [URL-e](#url-e)
  - [Opcje Import-u](#opcje-import-u)
  - [Misc Funkcje](#misc-funkcje)
  - [String-i](#string-i)
  - [Listy](#listy)
  - [Matematyczne Funkcje](#matematyczne-funkcje)
  - [Typy](#typy)
  - [Funkcje Kolorów](#funkcje-kolorów)
  - [Kanały Kolorów](#kanały-kolorów)
  - [Typy](#typy-1)
  - [Typy](#typy-2)

  - [Separatory](#separatory)
  - [URL-e](#url-e)
  - [Opcje import-u](#opcje-import-u)
  - [Misc funkcje](#misc-funkcje)
  - [String-i](#string-i)
  - [Listy](#listy)
  - [Matematyczne funkcje](#matematyczne-funkcje)
  - [Typy](#typy)
  - [Kolory](#kolory)
  - [Typy](#typy-1)
  - [Typy](#typy-2)

  - [Separatory](#separatory)
  - [URL-e](#url-e)
  - [Opcje import-u](#opcje-import-u)
  - [Misc funkcje](#misc-funkcje)
  - [String-i](#string-i)
  - [Listy](#listy)

  - [Separatory](#separatory)
  - [URL-e](#url-e)
  - [Opcje import-u](#opcje-import-u)
  - [Misc funkcje](#misc-funkcje)
  - [String-i](#string-i)
  - [Listy](#listy)

  - [Separatory](#separatory)
  - [URL-e](#url-e)

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

### Separatory

```py
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
```

### URL-e

```py
t_URL = r'url'
t_IMPORT = r'@import'
t_MEDIA = r'@media'
t_EXTEND = r':extend'
t_IMPORTANT = r'!important'
t_ARGUMENTS = r'@arguments'
t_REST = r'@rest'
```

### Opcje Import-u

```py
t_REFERENCE = r'reference'
t_INLINE = r'inline'
t_LESS = r'less'
t_CSS = r'css'
t_ONCE = r'once'
t_MULTIPLE = r'multiple'
t_OPTIONAL = r'optional'
```

### Misc Funkcje

```py
t_COLOR = r'color'
t_IMAGE_SIZE = r'image-size'
t_IMAGE_WIDTH = r'image-width'
t_IMAGE_HEIGHT = r'image-height'
t_CONVERT = r'convert'
t_DATA_URI = r'data_uri'
t_DEFAULT = r'default'
t_UNIT = r'unit'
t_GET_UNIT = r'get-unit'
t_SVG_GRADIENT = r'svg-gradient'
```

### String-i

```py
t_ESCAPE = r'escape'
t_E = r'e'
t_FORMAT = r'%'
t_REPLACE = r'replace'
```

### Listy

```py
t_LENGTH = r'length'
t_EXTRACT = r'extract'
t_RANGE = r'range'
t_EACH = r'each'
```

### Matematyczne Funkcje

```py
t_CEIL = r'ceil'
t_FLOOR = r'floor'
t_PERCENTAGE = r'percentage'
t_ROUND = r'round'
t_SRQT = r'sqrt'
t_ABS = r'abs'
t_SIN = r'sin'
t_ASIN = r'asin'
t_COS = r'cos'
t_ACOS = r'acos'
t_TAN = r'tan'
t_ATAN = r'atan'
t_PI = r'pi'
t_POW = r'pow'
t_MOD = r'mod'
t_MIN = r'min'
t_MAX = r'max'
```

### Typy

```py
t_ISNUMBER = r'isnumber'
t_ISSTRING = r'isstring'
t_ISCOLOR = r'iscolor'
t_ISKEYWORD = r'iskeyword'
t_ISURL = r'isurl'
t_ISPIXEL = r'ispixel'
t_ISEM = r'isem'
t_ISPERCENTAGE = r'ispercentage'
t_ISUNIT = r'isunit'
t_ISRULESET = r'isruleset'
t_ISDEFINED = r'isdefined'
```

### Funkcje Kolorów

```py
t_RGB = r'rgb'
t_RGBA = r'rgba'
t_ARGB = r'argb'
t_HSL = r'hsl'
t_HSLA = r'hsla'
t_HSV = r'hsv'
t_HSVA = r'hsva'
```

### Kanały Kolorów

```py
t_HUE = r'hue'
t_SATURATION = r'saturation'
t_LIGHTNESS = r'lightness'
t_HSVHUE = r'hsvhue'
t_HSVSATURATION = r'hsvsaturation'
t_HSVVALUE = r'hsvvalue'
t_RED = r'red'
t_GREEN = r'green'
t_BLUE = r'blue'
t_ALPHA = r'alpha'
t_LUMA = r'luma'
t_LUMINANCE = r'luminance'
```

### Operacje na Kolorach

```py
t_SATURATE = r'saturate'
t_DESATURATE = r'desaturate'
t_LIGHTEN = r'lighten'
t_DARKEN = r'darken'
t_FADEIN = r'fadein'
t_FADEOUT = r'fadeout'
t_FADE = r'fade'
t_SPIN = r'spin'
t_MIX = r'mix'
t_TINT = r'tint'
t_SHADE = r'shade'
t_GREYSCALE = r'greyscale'
t_CONTRAST = r'contrast'
```

### Blendowanie Kolorów

```py
t_MULTIPLY = r'multiply'
t_SCREEN = r'screen'
t_OVERLAY = r'overlay'
t_SOFTLIGHT = r'softlight'
t_HARDLIGHT = r'hardlight'
t_DIFFERENCE = r'difference'
t_EXCLUSION = r'exclusion'
t_AVERAGE = r'average'
t_NEGATION = r'negation'
```

### Łączniki

```py
t_WHEN = r'when'
t_NOT = r'not'
t_AND = r'and'
```

### Literały Stringów

```py
t_STRING = r''

def t_NUMBER(t):
  r'[+-]?([0-9]*[.])?([0-9])+'
  t.value = float(t.value)
  return t

t_Color = r'^#(([0-9]|[a-f]|[A-F]){3}|([0-9]|[a-f]|[A-F]){5}|([0-9]|[a-f]|[A-F]){6})$'
```

### Linia Stringu

```py
def t_SL_COMMENT(t):
  r'\/\/.*?'
  pass
```

### Wieloliniowy String

```py
def t_COMMENT(t):
  r'\/\*((\n\*)*(.*?))*\*\/'
  pass
```

### Pusta Przestrzeń

```py
def t_WS(t):
  r' |\t|\n|\r|\r\n'
  pass
```

### Nulle I Tym Podobne

```py
t_NULL_ = r'null'
t_IN = r'in'
t_Unit = r'%|px|cm|mm|in|pt|pc|em|ex|deg|rad|grad|ms|s|hz|khz'
t_Ellipsis = r'...'
```
