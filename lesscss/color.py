import operator

import colorsys
import re
from six import string_types
from . import utilities
from htmlcss import colors


class Color:
    def process(self, expression):
        a, o, b = expression
        c1 = self._hextorgb(a)
        c2 = self._hextorgb(b)
        r = ['#']
        for i in range(3):
            v = self.operate(c1[i], c2[i], o)
            if v > 0xff:
                v = 0xff
            if v < 0:
                v = 0
            r.append("%02x" % int(v))
        return ''.join(r)

    def operate(self, left, right, operation):
        operation = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }.get(operation)
        return operation(left, right)

    def rgb(self, *args):
        if len(args) == 4:
            args = args[:3]
        if len(args) == 3:
            try:
                return self._rgbatohex(list(map(int, args)))
            except ValueError:
                if all((a for a in args
                        if a[-1] == '%' and 100 >= int(a[:-1]) >= 0)):
                    return self._rgbatohex(
                        [int(a[:-1]) * 255 / 100.0 for a in args])
        raise ValueError('Illegal color values')

    def rgba(self, *args):
        if len(args) == 4:
            try:
                falpha = float(list(args)[3])
                if falpha > 1:
                    args = args[:3]
                if falpha == 0:
                    values = self._rgbatohex_raw(list(map(int, args)))
                    return "rgba(%s)" % ','.join([str(a) for a in values])
                return self._rgbatohex(list(map(int, args)))
            except ValueError:
                if all((a for a in args
                        if a[-1] == '%' and 100 >= int(a[:-1]) >= 0)):
                    alpha = list(args)[3]
                    if alpha[-1] == '%' and float(alpha[:-1]) == 0:
                        values = self._rgbatohex_raw(
                            [int(a[:-1]) * 255 / 100.0 for a in args])
                        return "rgba(%s)" % ','.join([str(a) for a in values])
                    return self._rgbatohex(
                        [int(a[:-1]) * 255 / 100.0 for a in args])
        raise ValueError('Illegal color values')

    def argb(self, *args):
        if len(args) == 1 and type(args[0]) is str:
            match = re.match(r'rgba\((.*)\)', args[0])
            if match:
                rgb = re.sub(r'\s+', '', match.group(1)).split(',')
            else:
                rgb = list(self._hextorgb(args[0]))
        else:
            rgb = list(args)
        if len(rgb) == 3:
            return self._rgbatohex([255] + list(map(int, rgb)))
        elif len(rgb) == 4:
            rgb = [rgb.pop()] + rgb
            try:
                fval = float(list(rgb)[0])
                if fval > 1:
                    rgb = [255] + rgb[1:]
                elif 1 >= fval >= 0:
                    rgb = [
                              fval * 256
                          ] + rgb[1:]
                else:
                    rgb = [0] + rgb[1:]
                return self._rgbatohex(list(map(int, rgb)))
            except ValueError:
                if all((a for a in rgb
                        if a[-1] == '%' and 100 >= int(a[:-1]) >= 0)):
                    return self._rgbatohex(
                        [int(a[:-1]) * 255 / 100.0 for a in rgb])
        raise ValueError('Illegal color values')

    def hsl(self, *args):
        if len(args) == 4:
            return self.hsla(*args)
        elif len(args) == 3:
            h, s, l = args
            rgb = colorsys.hls_to_rgb(
                int(h) / 360.0, utilities.pc_or_float(l), utilities.pc_or_float(s))
            color = (utilities.convergent_round(c * 255) for c in rgb)
            return self._rgbatohex(color)
        raise ValueError('Illegal color values')

    def hsla(self, *args):
        if len(args) == 4:
            h, s, l, a = args
            rgb = colorsys.hls_to_rgb(
                int(h) / 360.0, utilities.pc_or_float(l), utilities.pc_or_float(s))
            color = [float(utilities.convergent_round(c * 255)) for c in rgb]
            color.append(utilities.pc_or_float(a))
            return "rgba(%s,%s,%s,%s)" % tuple(color)
        raise ValueError('Illegal color values')

    def hue(self, color, *args):
        if color:
            h, l, s = self._hextohls(color)
            return utilities.convergent_round(h * 360.0, 3)
        raise ValueError('Illegal color values')

    def saturation(self, color, *args):
        if color:
            h, l, s = self._hextohls(color)
            return s * 100.0
        raise ValueError('Illegal color values')

    def lightness(self, color, *args):
        if color:
            h, l, s = self._hextohls(color)
            return l * 100.0
        raise ValueError('Illegal color values')

    def opacity(self, *args):
        pass

    def lighten(self, color, diff, *args):
        if color and diff:
            return self._ophsl(color, diff, 1, operator.add)
        raise ValueError('Illegal color values')

    def darken(self, color, diff, *args):
        if color and diff:
            return self._ophsl(color, diff, 1, operator.sub)
        raise ValueError('Illegal color values')

    def saturate(self, color, diff, *args):
        if color and diff:
            return self._ophsl(color, diff, 2, operator.add)
        raise ValueError('Illegal color values')

    def desaturate(self, color, diff, *args):
        if color and diff:
            return self._ophsl(color, diff, 2, operator.sub)
        raise ValueError('Illegal color values')

    def _clamp(self, value):
        return min(1, max(0, value))

    def greyscale(self, color, *args):
        if color:
            return self.desaturate(color, 100.0)
        raise ValueError('Illegal color values')

    def grayscale(self, color, *args):
        return self.greyscale(color, *args)

    def spin(self, color, degree, *args):
        if color and degree:
            if isinstance(degree, string_types):
                degree = float(degree.strip('%'))
            h, l, s = self._hextohls(color)
            h = ((h * 360.0) + degree) % 360.0
            h = 360.0 + h if h < 0 else h
            rgb = colorsys.hls_to_rgb(h / 360.0, l, s)
            color = (utilities.convergent_round(c * 255) for c in rgb)
            return self._rgbatohex(color)
        raise ValueError('Illegal color values')

    def mix(self, color1, color2, weight=50, *args):
        if color1 and color2:
            if isinstance(weight, string_types):
                weight = float(weight.strip('%'))
            weight = ((weight / 100.0) * 2) - 1
            rgb1 = self._hextorgb(color1)
            rgb2 = self._hextorgb(color2)
            alpha = 0
            w1 = (((weight if weight * alpha == -1 else weight + alpha) /
                   (1 + weight * alpha)) + 1)
            w1 = w1 / 2.0
            w2 = 1 - w1
            rgb = [
                rgb1[0] * w1 + rgb2[0] * w2,
                rgb1[1] * w1 + rgb2[1] * w2,
                rgb1[2] * w1 + rgb2[2] * w2,
            ]
            return self._rgbatohex(rgb)
        raise ValueError('Illegal color values')

    def fmt(self, color):
        if utilities.is_color(color):
            color = color.lower().strip('#')
            if len(color) in [3, 4]:
                color = ''.join([c * 2 for c in color])
            return '#%s' % color
        raise ValueError('Cannot format non-color')

    def _rgbatohex_raw(self, rgba):
        values = [
            "%x" % int(v)
            for v in [0xff if h > 0xff else 0 if h < 0 else h for h in rgba]
        ]
        return values

    def _rgbatohex(self, rgba):
        return '#%s' % ''.join([
            "%02x" % int(v)
            for v in [0xff if h > 0xff else 0 if h < 0 else h for h in rgba]
        ])

    def _hextorgb(self, hex):
        if hex.lower() in colors.lessColors:
            hex = colors.lessColors[hex.lower()]
        hex = hex.strip()
        if hex[0] == '#':
            hex = hex.strip('#').strip(';')
            if len(hex) == 3:
                hex = [c * 2 for c in hex]
            else:
                hex = [hex[i:i + 2] for i in range(0, len(hex), 2)]
            return tuple(int(c, 16) for c in hex)
        try:
            return [int(hex, 16)] * 3
        except:
            return [float(hex)] * 3

    def _hextohls(self, hex):
        rgb = self._hextorgb(hex)
        return colorsys.rgb_to_hls(*[c / 255.0 for c in rgb])

    def _ophsl(self, color, diff, idx, operation):
        if isinstance(diff, string_types):
            diff = float(diff.strip('%'))
        hls = list(self._hextohls(color))
        hls[idx] = self._clamp(operation(hls[idx], diff / 100.0))
        rgb = colorsys.hls_to_rgb(*hls)
        color = (utilities.away_from_zero_round(c * 255) for c in rgb)
        return self._rgbatohex(color)