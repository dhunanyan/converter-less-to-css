<h1 align="center">  Kompilator Less.js do CSS </h1>

## Spis treści

- [Spis treści](#spis-treści)
- [Informacje o projekcie](#informacje-o-projekcie)
- [Spis tokenów](#spis-tokenów)
  - [Tokeny](#tokeny)
  - [Literały](#literały)
- [Klasa Errorów](#klasa-errorów)
  - [Rejestrowanie Errorów](#rejestrowanie-errorów)
  - [Printowanie Errorów](#printowanie-errorów)
- [Gramatyka](#gramatyka)
- [Struktura Drzewiasta Projektu](#struktura-drzewiasta-projektu)
- [Technologie i Biblioteki](#technologie-i-biblioteki)
- [Instrukcja Uruchomienia Projektu](#instrukcja-uruchomienia-projektu)
  - [Instalacja Potrzebnych Bibliotek:](#instalacja-potrzebnych-bibliotek)
  - [Utworzenie Pliku Inputu](#utworzenie-pliku-inputu)
  - [Uruchomienie Projektu](#uruchomienie-projektu)
  - [Output](#output)
- [Przykładowe Testy](#przykładowe-testy)
  - [Input №1](#input-1)
  - [Input №2](#input-2)
  - [Input №3](#input-3)
  - [Input №4](#input-4)
  - [Input №5](#input-5)
  - [Input №6](#input-6)
  - [Input №7](#input-7)
  - [Input №8](#input-8)
  - [Input №9](#input-9)

## Informacje o projekcie

- Autorzy:

  - Maciej Ciepał `maciejciepal@student.agh.edu.pl`
  - Davit Hunanyan `hunanyan@student.agh.edu.pl`

- Główne cele i założenia projektu:

  - Translacja kodu z Less.js do CSS

- Język implementacji:

  - Python

## Spis tokenów

### Tokeny

```
css_comment
css_string
css_important
css_vendor_hack
css_uri
css_ms_filter
css_keyframe_selector
css_media_feature
less_comment
less_open_format
less_when
less_and
less_not
t_ws
t_popen
t_pclose
t_semicolon
t_tilde
t_colon
t_comma
t_eopen
t_eclose
t_isopen
t_isclose
t_bopen
t_bclose
css_class
css_id
css_dom
css_property
css_vendor_property
css_user_property
css_ident
css_number
css_color
css_media_type
css_filter
less_variable
t_and
t_not
t_only
```

### Literały

```
<
>
=
%
!
/
*
-
+
&
```

### Zarezerwowane Nazwy Zmiennych

> W języku Less.js nazwy zmiennych zaczynają się od znaku ``@``, natommiast w CSS są nazwy zarezerwowane takie jak ``@media``, ``@keyframes`` i tym podobne, zatem trzeba zablokowaćich użycie jako nazwy. Poniżej jest przedstawiona lista zarezerwowanych tokenów.

```js
tokens = {
    '@media': 'css_media',
    '@page': 'css_page',
    '@import': 'css_import',
    '@charset': 'css_charset',
    '@font-face': 'css_font_face',
    '@namespace': 'css_namespace',
    '@keyframes': 'css_keyframes',
    '@-moz-keyframes': 'css_keyframes',
    '@-webkit-keyframes': 'css_keyframes',
    '@-ms-keyframes': 'css_keyframes',
    '@-o-keyframes': 'css_keyframes',
    '@viewport': 'css_viewport',
    '@-ms-viewport': 'css_viewport',
    '@arguments': 'less_arguments',
}
```

## Klasa Errorów

### Rejestrowanie Errorów
```py
class ErrorRegister(object):
    def __init__(self):
        self.errors = []

    def register(self, error):
        self.errors.append(error)

    def __close__(self):
        if self.errors:
            raise CompilationError("\n".join(self.errors))

    close = __close__
```

### Printowanie Errorów

```py
class PrintErrorRegister(object):
    def __init__(self):
        self.has_errored = False

    def register(self, error):
        self.has_errored = True
        color = '\x1b[31m' if error[0] == 'E' else '\x1b[33m'
        print("%s%s\x1b[0m" % (color, error), end='\x1b[0m', file=sys.stderr)

    def __close__(self):
        pass

    close = __close__

```

## Gramatyka

```
tunit                         : unit_list

unit_list                     : unit_list unit
                              | unit

unit                          : statement
                              | variable_decl
                              | block_decl
                              | mixin_decl
                              | call_mixin
                              | import_statement

statement                     : css_charset t_ws css_string t_semicolon
                              | css_namespace t_ws css_string t_semicolon

statement                     : css_namespace t_ws word css_string t_semicolon

import_statement              : css_import t_ws string t_semicolon
                              | css_import t_ws css_string t_semicolon
                              | css_import t_ws css_string media_query_list t_semicolon
                              | css_import t_ws fcall t_semicolon
                              | css_import t_ws fcall media_query_list t_semicolon

block_decl                    : block_open declaration_list brace_close

block_decl                    : identifier t_semicolon

block_open                    : identifier brace_open

block_open                    : media_query_decl brace_open

block_open                    : css_font_face t_ws brace_open

block_open                    : css_keyframe_selector brace_open
                              | number brace_open

mixin_decl                    : open_mixin declaration_list brace_close

open_mixin                    : identifier t_popen mixin_args_list t_pclose brace_open
                              | identifier t_popen mixin_args_list t_pclose mixin_guard brace_open

 mixin_guard                  : less_when mixin_guard_cond_list

mixin_guard_cond_list         : mixin_guard_cond_list t_comma mixin_guard_cond
                              | mixin_guard_cond_list less_and mixin_guard_cond

mixin_guard_cond_list         : mixin_guard_cond

mixin_guard_cond              : less_not t_popen argument mixin_guard_cmp argument t_pclose
                              | less_not t_popen argument t_pclose

mixin_guard_cond              : t_popen argument mixin_guard_cmp argument t_pclose
                              | t_popen argument t_pclose

mixin_guard_cmp               : '>'
                              | '<'
                              | '='
                              | '>' '='
                              | '=' '<'

call_mixin                    : identifier t_popen mixin_args_list t_pclose t_semicolon

mixin_args_list               : less_arguments

mixin_args_list               : mixin_args_list t_comma mixin_args
                              | mixin_args_list t_semicolon mixin_args

mixin_args_list               : mixin_args

mixin_args                    : mixin_args argument

mixin_args                    : argument
                              | mixin_kwarg

mixin_args                    : empty

mixin_kwarg                   : variable t_colon mixin_kwarg_arg_list

mixin_kwarg_arg_list          : mixin_kwarg_arg_list argument

mixin_kwarg_arg_list          : argument

declaration_list              : declaration_list declaration
                              | declaration
                              | empty

declaration                   : variable_decl
                              | property_decl
                              | block_decl
                              | mixin_decl
                              | call_mixin
                              | import_statement

variable_decl                 : variable t_colon style_list t_semicolon

property_decl                 : prop_open style_list t_semicolon
                              | prop_open style_list css_important t_semicolon
                              | prop_open empty t_semicolon

property_decl                 : prop_open less_arguments t_semicolon

prop_open                     : '*' prop_open

prop_open                     : property t_colon
                              | vendor_property t_colon
                              | user_property t_colon
                              | word t_colon

style_list                    : style_list style
                              | style_list t_comma style
                              | style_list t_ws style

style_list                    : style

style                         : expression
                              | string
                              | word
                              | property
                              | vendor_property
                              | estring

identifier                    : identifier_list
                              | page
                              | page filter

identifier                    : t_popen estring t_pclose

identifier_list               : identifier_list t_comma identifier_group

identifier_list               : identifier_group

identifier_list               : css_keyframes t_ws css_ident
                              | css_keyframes t_ws css_ident t_ws

identifier_list               : css_viewport
                              css_viewport t_ws
                           
identifier_group              : identifier_group child_selector ident_parts
                              | identifier_group '+' ident_parts
                              | identifier_group general_sibling_selector ident_parts
                              | identifier_group '*'

identifier_group              : ident_parts

ident_parts                   : ident_parts ident_part
                              | ident_parts filter_group

ident_parts                   : ident_part
                              | selector
                              | filter_group

 media_query_decl             : css_media t_ws
                              | css_media t_ws media_query_list

media_query_list              : media_query_list t_comma media_query

media_query_list              : media_query

media_query                   : media_type
                              | media_type media_query_expression_list
                              | not media_type
                              | not media_type media_query_expression_list
                              | only media_type
                              | only media_type media_query_expression_list

media_query                   : media_query_expression media_query_expression_list
                              | media_query_expression

media_query_expression_list   : media_query_expression_list and media_query_expression
                              | and media_query_expression

media_query_expression        : t_popen css_media_feature t_pclose
                              | t_popen css_media_feature t_colon media_query_value t_pclose

media_query_value             : number
                              | variable
                              | word
                              | color
                              | expression

selector                      : '*'
                              | '+'
                              | child_selector
                              | general_sibling_selector

ident_part                    : iclass
                              | id
                              | dom
                              | combinator
                              | color

ident_part                    : combinator vendor_property

filter_group                  : filter_group filter

filter_group                  : filter

filter                        : css_filter
                              | css_filter t_ws
                              | t_colon word
                              | t_colon vendor_property
                              | t_colon vendor_property t_ws
                              | t_colon css_property
                              | t_colon css_property t_ws
                              | t_colon css_filter
                              | t_colon css_filter t_ws
                              | t_colon t_colon word
                              | t_colon t_colon vendor_property

ms_filter                     : css_ms_filter
                              | css_ms_filter t_ws

fcall                         : word t_popen argument_list t_pclose
                              | property t_popen argument_list t_pclose
                              | vendor_property t_popen argument_list t_pclose
                              | less_open_format argument_list t_pclose
                              | ms_filter t_popen argument_list t_pclose

argument_list                 : empty

argument_list                 : argument_list argument
                              | argument_list t_comma argument

argument_list                 : argument

argument                      : expression
                              | string
                              | estring
                              | word
                              | id
                              | css_uri
                              | css_user_property
                              | '='
                              | fcall

expression                    : expression '+' expression
                              | expression '-' expression
                              | expression '/' expression
                              | expression '*' expression
                              | word '/' expression

expression                    : '-' t_popen expression t_pclose

expression                    : t_popen expression t_pclose

expression                    : factor

factor                        : color
                              | number
                              | variable
                              | css_dom
                              | fcall

estring                       : t_eopen style_list t_eclose
                              | t_eopen identifier_list t_eclose

string_part                   : variable
                              | css_string

string_part_list              : string_part_list string_part

string_part_list              : string_part

string                        : t_isopen string_part_list t_isclose

string                        : css_string

variable                      : '-' variable

variable                      : t_popen variable t_pclose

variable                      : less_variable
                              | less_variable t_ws

color                         : css_color
                              | css_color t_ws

number                        : css_number
                              | css_number t_ws

dom                           : css_dom
                              | css_dom t_ws

word                          : css_ident
                              | css_ident t_ws

class                         : css_class
                              | css_class t_ws

iclass_part                   : less_variable
                              | less_variable t_ws
                              | class

iclass_part_list              : iclass_part_list iclass_part

iclass_part_list              : iclass_part

iclass                        : iclass_part_list

id                            : css_id
                              | css_id t_ws

property                      : css_property
                              | css_property t_ws

page                          : css_page
                              | css_page t_ws

vendor_property               : css_vendor_property
                              | css_vendor_property t_ws

user_property                 : css_user_property
                              | css_user_property t_ws

media_type                    : css_media_type
                              | css_media_type t_ws

combinator                    : '&' t_ws
                              | '&'

child_selector                : '>' t_ws
                              | '>'

general_sibling_selector      : t_tilde t_ws
                              | t_tilde

brace_open                    : t_bopen

brace_close                   : t_bclose

and                           : t_and t_ws
                              | t_and
                              
not                           : t_not t_ws
                              | t_not

only                          : t_only t_ws
                              | t_only

empty                         :

error
```

## Struktura Drzewiasta Projektu

    .
    ├── compiler
    |     ├── __init__.py
    |     └── compiler.py
    ├── htmlcss
    |     ├── __init__.py
    |     ├── colors.py
    |     ├── css.py
    |     ├── html.py
    |     └── reserved.py
    ├── lesscss
    |     ├── __init__.py
    |     ├── color.py
    |     ├── format.py
    |     ├── lexer.py
    |     ├── parser.py
    |     ├── scope.py
    |     ├── tokens.py
    |     └── utilities.py
    ├── lib
    |     ├── __init__.py
    |     ├── block.py
    |     ├── call.py
    |     ├── deferred.py
    |     ├── expression.py
    |     ├── identifier.py
    |     ├── import_.py
    |     ├── keyframe_selector.py
    |     ├── mixin.py
    |     ├── negated_expression.py
    |     ├── node.py
    |     ├── property.py
    |     ├── statement.py
    |     └── variable.py
    ├── exceptions.py
    ├── main.py
    └── README.md

## Technologie i Biblioteki

W projekcie zostały użyte poniższe technologie:

- Python 3.9
- PLY (Python Lex-Yacc)
- six 1.16.0

## Instrukcja Uruchomienia Projektu

### Instalacja Potrzebnych Bibliotek:

- ```bash
    pip install six
  ```
- ```bash
    pip install ply
  ```

### Utworzenie Pliku Inputu

Wymagany jest plik inputu z rzoszerzeniem `.less` w głównym katalogu zawierający `input` w języku `LESS`

- `np: example.less`

### Uruchomienie Projektu

Uruchamiamy projekt poprzez wpisanie komendy w terminal, znajdując się w katalogu głównym:

- Jeżeli chcemy, aby `output` był wypisany to trzeba uruchomić projekt za pomocą poniższej komendy (gdzie `example.less` jest to wyżej wspomniany plik zawierający `input` w `LESS`):

```bash
   python main.py example.less
```

- Jeżeli natomiast chcemy, aby `output` był wypisany w osobnym pliku, to trzeba uruchomić projekt za pomocą poniższej komendy (gdzie gdzie `example.less` jest to wyżej wspomniany plik zawierający `input` w `LESS`, natomiast `'./your_path.css'` jest scieżką docelową do `outputu` w `CSS`):

```bash
   python main.py example.less './your_path.css'
```

### Output

Skonwertowany kod będzie wypisany w terminalu lub w pliku docelowym `outputu` - w zależności od wyboru powyższych komend.

## Przykładowe Testy

W katalogu `samples` znajdują się przykładowe pliki które mają pewien `input` oraz `oczekiwany output`. Zalecane jest prztestować pliki zawarte w tym katalogu, aby upewnić się, że projekt jest prawidłowy skonfigurowany.

### Input №1

- Zawartość pliku `samples/input_1.less`:

  ```less
  // Variables
  @my-selector: banner;

  // Usage
  .@{my-selector} {
    font-weight: bold;
    line-height: 40px;
    margin: 0 auto;
  }
  ```

- Uruchomienie konwertera podając `input` zawarty w `samples/input_1.less`:

```bash
  python main.py samples/input_1.less
```

- Oczekiwany `output`:

  ```css
  .banner {
    font-weight: bold;
    line-height: 40px;
    margin: 0 auto;
  }
  ```

### Input №2

- Zawartość pliku `samples/input_2.less`:

  ```less
  .lazy-eval {
    width: @var;
  }

  @var: @a;
  @a: 9%;
  ```

- Uruchomienie konwertera podając `input` zawarty w `samples/input_2.less`:

```bash
python main.py samples/input_2.less
```

- Oczekiwany `output`:

  ```css
  .lazy-eval {
    width: 9%;
  }
  ```

### Input №3

- Zawartość pliku `samples/input_3.less`:

  ```less
  // Variables
  @link-color: #428bca; // sea blue
  @link-color-hover: @link-color;

  // Usage
  a,
  .link {
    color: @link-color;
  }
  a:hover {
    color: @link-color-hover;
  }
  .widget {
    color: #fff;
    background: @link-color;
  }
  ```

- Uruchomienie konwertera podając `input` zawarty w `samples/input_3.less`:

```bash
python main.py samples/input_3.less
```

- Oczekiwany `output`:

  ```css
  a,
  .link {
    color: #428bca;
  }
  a:hover {
    color: #3071a9;
  }
  .widget {
    color: #ffffff;
    background: #428bca;
  }
  ```

### Input №4

- Zawartość pliku `samples/input_4.less`:

  ```less
  @header-font: Arial;
  h1 {
    font-family: @header-font;
  }
  .concrete {
    font-family: @header-font;
  }
  ```

- Uruchomienie konwertera podając `input` zawarty w `samples/input_4.less`:

```bash
python main.py samples/input_4.less
```

- Oczekiwany `output`:

  ```css
  h1 {
    font-family: Arial;
  }
  .concrete {
    font-family: Arial;
  }
  ```

### Input №5

- Zawartość pliku `samples/input_5.less`:

  ```less
  @var: 0;
  .class {
    @var: 1;
    .brass {
      @var: 2;
      three: @var;
      @var: 3;
    }
    one: @var;
  }
  ```

- Uruchomienie konwertera podając `input` zawarty w `samples/input_5.less`:

```bash
python main.py samples/input_5.less
```

- Oczekiwany `output`:

  ```css
  .class {
    one: 1;
  }
  .class .brass {
    three: 3;
  }
  ```

### Input №6

- Zawartość pliku `samples/input_6.less`:

  ```less
  a {
    color: blue;
    &:hover {
      color: green;
    }
  }
  ```

- Uruchomienie konwertera podając `input` zawarty w `samples/input_6.less`:

```bash
python main.py samples/input_6.less
```

- Oczekiwany `output`:

  ```css
  a {
    color: blue;
  }

  a:hover {
    color: green;
  }
  ```

### Input №7

- Zawartość pliku `samples/input_7.less`:

  ```less
  .header {
    .menu {
      border-radius: 5px;
      .no-borderradius & {
        background-image: url("images/button-background.png");
      }
    }
  }
  ```

- Uruchomienie konwertera podając `input` zawarty w `samples/input_7.less`:

```bash
python main.py samples/input_7.less
```

- Oczekiwany `output`:

  ```css
  .header .menu {
    border-radius: 5px;
  }
  .no-borderradius .header .menu {
    background-image: url("images/button-background.png");
  }
  ```

### Input №8

- Zawartość pliku `samples/input_8.less`:

  ```less
  .my-mixin {
    color: black;
  }
  .my-other-mixin() {
    background: white;
  }
  .class {
    .my-mixin();
    .my-other-mixin();
  }
  ```

- Uruchomienie konwertera podając `input` zawarty w `samples/input_8.less`:

```bash
python main.py samples/input_8.less
```

- Oczekiwany `output`:

  ```css
  .my-mixin {
    color: black;
  }
  .class {
    color: black;
    background: white;
  }
  ```

### Input №9

- Zawartość pliku `samples/input_9.less`:

  ```less
  .my-mixin {
    color: black;
  }
  .my-other-mixin() {
    background: white;
  }
  .class {
    .my-mixin();
    .my-other-mixin();
  }
  ```

- Uruchomienie konwertera podając `input` zawarty w `samples/input_9.less`:

```bash
python main.py samples/input_9.less
```

- Oczekiwany `output`:

  ```css
  button:hover {
    border: 1px solid red;
  }
  ```
