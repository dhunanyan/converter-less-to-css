from ply import lex

class LessLexer(object):
  tokens = (
    'NULL_',
    'IN',
    'Unit',
    'Ellipsis',
    'LPAREN',
    'RPAREN',
    'BlockStart',
    'BlockEnd',
    'LBRACK',
    'RBRACK',
    'GT',
    'LT',
    'TIL',
    'COLON',
    'SEMI',
    'COMMA',
    'DOT',
    'DOLLAR',
    'AT',
    'PARENTREF',
    'HASH',
    'COLONCOLON',
    'PLUS',
    'TIMES',
    'DIV',
    'MINUS',
    'PERC',
    'EQEQ',
    'GTEQ',
    'LTEQ',
    'NOTEQ',
    'EQ',
    'PIPE_EQ',
    'TILD_EQ',
    'URL',
    'IMPORT',
    'MEDIA',
    'EXTEND',
    'IMPORTANT',
    'ARGUMENTS',
    'REST',
    'REFERENCE',
    'INLINE',
    'LESS',
    'CSS',
    'ONCE',
    'MULTIPLE',
    'WHEN',
    'NOT',
    'AND',
    'Identifier',
    'StringLiteral',
    'Number',
    'Color',
    'WS',
    'SL_COMMENT',
    'COMMENT',
    'FUNCTION_NAME',
    'COLOR',
    'CONVERT',
    'DATA_URI',
    'DEFAULT',
    'UNIT',
    'GET_UNIT',
    'SVG_GRADIENT',
    'ESCAPE',
    'E',
    'FORMAT',
    'REPLACE',
    'LENGTH',
    'EXTRACT',
    'CEIL',
    'FLOOR',
    'PERCENTAGE',
    'ROUND',
    'SQRT',
    'ABS',
    'SIN',
    'ASIN',
    'COS',
    'ACOS',
    'TAN',
    'ATAN',
    'PI',
    'POW',
    'MOD',
    'MIN',
    'MAX',
    'ISNUMBER',
    'ISSTRING',
    'ISCOLOR',
    'ISKEYWORD',
    'ISURL',
    'ISPIXEL',
    'ISEM',
    'ISPERCENTAGE',
    'ISUNIT',
    'RGB',
    'RGBA',
    'ARGB',
    'HSL',
    'HSLA',
    'HSV',
    'HSVA',
    'HUE',
    'SATURATION',
    'LIGHTNESS',
    'HSVHUE',
    'HSVSATURATION',
    'HSVVALUE',
    'RED',
    'GREEN',
    'BLUE',
    'ALPHA',
    'LUMA',
    'LUMINANCE',
    'SATURATE',
    'DESATURATE',
    'LIGHTEN',
    'DARKEN',
    'FADEIN',
    'FADEOUT',
    'FADE',
    'SPIN',
    'MIX',
    'GREYSCALE',
    'CONTRAST',
    'MULTIPLY',
    'SCREEN',
    'OVERLAY',
    'SOFTLIGHT',
    'HARDLIGHT',
    'DIFFERENCE',
    'EXCLUSION',
    'AVERAGE',
    'NEGATION',
  )

t_NULL_ = r'null'
t_IN = r'in'
t_Unit = r'%|px|cm|mm|in|pt|pc|em|ex|deg|rad|grad|ms|s|hz|khz'
t_Ellipsis = r'...'

# MIXIN GUARDS
# =================================================================
t_WHEN = r'when'
t_NOT = r'not'
t_AND = r'and'

# STRING LITERALS
# =================================================================
t_STRING = r''

def t_NUMBER(t):
  r'[+-]?([0-9]*[.])?([0-9])+'
  t.value = float(t.value)
  return t

t_Color = r'^#(([0-9]|[a-f]|[A-F]){3}|([0-9]|[a-f]|[A-F]){5}|([0-9]|[a-f]|[A-F]){6})$'

# WHITESPACE - ignored
# =================================================================
def t_WS(t):
  r' |\t|\n|\r|\r\n'
  pass

# SINGLE-LINE COMMENT
# =================================================================
def t_SL_COMMENT(t):
  r'\/\/.*?'
  pass

# MULTIPLE-LINE COMMENT
# =================================================================
def t_COMMENT(t):
  r'\/\*((\n\*)*(.*?))*\*\/'
  pass


# SEPARATORS
# =================================================================
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

# URLS
# http://lesscss.org/features/#variables-feature-urls
# =================================================================
t_URL = r'url'
t_IMPORT = r'@import'
t_MEDIA = r'@media'
t_EXTEND = r':extend'
t_IMPORTANT = r'!important'
t_ARGUMENTS = r'@arguments'
t_REST = r'@rest'

# IMPORT OPTIONS
# http://lesscss.org/features/#import-options
t_REFERENCE = r'reference'
t_INLINE = r'inline'
t_LESS = r'less'
t_CSS = r'css'
t_ONCE = r'once'
t_MULTIPLE = r'multiple'
t_OPTIONAL = r'optional'

# MIXIN GUARDS
# =================================================================


# FUNCTIONS
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# MISC
# http://lesscss.org/functions/#misc-functions
# =================================================================
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

# STRING
# http://lesscss.org/functions/#string-functions
# =================================================================
t_ESCAPE = r'escape'
t_E = r'e'
t_FORMAT = r'%'
t_REPLACE = r'replace'

# LIST
# http://lesscss.org/functions/#list-functions
# =================================================================
t_LENGTH = r'length'
t_EXTRACT = r'extract'
t_RANGE = r'range'
t_EACH = r'each'

# MATH
# http://lesscss.org/functions/#math-functions
# =================================================================
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

# TYPE
# http://lesscss.org/functions/#type-functions
# =================================================================
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

# COLOR
# http://lesscss.org/functions/#color-definition
# =================================================================
t_RGB = r'rgb'
t_RGBA = r'rgba'
t_ARGB = r'argb'
t_HSL = r'hsl'
t_HSLA = r'hsla'
t_HSV = r'hsv'
t_HSVA = r'hsva'

# COLOR CHANNEL
# http://lesscss.org/functions/#color-channel
# =================================================================
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

# COLOR OPERATION
# http://lesscss.org/functions/#color-operations
# =================================================================
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

# COLOR BLENDING
# http://lesscss.org/functions/#color-blending
# =================================================================
t_MULTIPLY = r'multiply'
t_SCREEN = r'screen'
t_OVERLAY = r'overlay'
t_SOFTLIGHT = r'softlight'
t_HARDLIGHT = r'hardlight'
t_DIFFERENCE = r'difference'
t_EXCLUSION = r'exclusion'
t_AVERAGE = r'average'
t_NEGATION = r'negation'