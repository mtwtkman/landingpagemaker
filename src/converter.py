# -*- coding: utf-8 -*-
import re


HEADER = re.compile(r'(#{1,6})(.*)')
colors = '|'.join(['red', 'blue'])
COLOR = re.compile(
    (r'('
     'rgb\('
     '(?:(?:[0-9]|[0-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),?){{3}}\)|'
     '#(?:[0-9a-fA-F]{{6}}|[0-9a-fA-F]{{3}})|'
     '{colors}'
     ')'.format(colors=colors))
)
FONT_SIZE = re.compile(r'(\d+)(?:pt)?')
IMG_SRC = re.compile(r'(?:img=)([\w\.]+)')


def _escape(body):
    return body.replace('\\', '')


def _span(body):
    # Convert to span tag.
    return '<span>{body}</span>'.format(body=_escape(body))


def _hash(text):
    # Convert to header tag.
    headers, body = HEADER.match(text).groups()
    return '<h{n}>{body}</h{n}>'.format(
        n=len(headers),
        body=_escape(body)
    )


def _sign_converter(text, sign):
    index_range = len(text) - 1
    end_index = index_range - text[::-1].index(sign)
    if end_index == 0:
        return _span(text)
    body = text[1:end_index]
    left = text[end_index+1:]
    color = ''
    size = ''
    for x in left.split(':'):
        if not x:
            continue
        try:
            color = 'color:' + COLOR.match(x).groups()[0] + ';'
        except AttributeError:
            pass
        try:
            size = 'font-size:' + FONT_SIZE.match(x).groups()[0] + 'pt;'
        except AttributeError:
            pass
    style = {
        '*': 'font-weight:bold;',
        '_': 'text-decoration:underline;',
        '|': 'background-color:yellow;'
    }.get(sign)
    return '<span style="{style}{color}{size}">{body}</span>'.format(
        style=style,
        color=color,
        size=size,
        body=body
    )


def _img(l, align=''):
    src = re.match(IMG_SRC, l)
    attrs = []
    if src:
        attrs.append('src="{}"'.format(src.groups()[0]))
    if ':' in l:
        s = l.split(':')[1]
        if 'x' in s:
            h = 'x'
            s = s.split('x')
        else:
            h = s[0]
            s = [s[1:]]
        attrs.append({
            'w': 'width="{}"',
            'h': 'height="{}"',
            'x': 'width="{}" height="{}"'
         }.get(h).format(*s))
    if align:
        attrs.append('align="{}"'.format(align))
    return '<img {}>'.format(' '.join(attrs))


def parser(lines):
    if not isinstance(lines, (list, tuple)):
        lines = [lines]

    result = []
    for l in lines:
        l.replace('\n', '<br>')
        l = l.strip()
        if l.startswith('#'):
            result.append(_hash(l))
        elif l.startswith('\\'):
            result.append(_span(l))
        elif l == '-':
            result.append('<hr>')
        elif l.startswith('*'):
            result.append(_sign_converter(l, '*'))
        elif l.startswith('_'):
            result.append(_sign_converter(l, '_'))
        elif l.startswith('|'):
            result.append(_sign_converter(l, '|'))
        elif l.startswith('img'):
            result.append(_img(l))
        elif l.startswith('>') or l.startswith('<'):
            result.append(_img(l[1:], {'>': 'right', '<': 'left'}.get(l[0])))
        else:
            result.append(_span(l))
    return '<p></p>'.join(result)


HTML = '''<!doctype>
<html>
  <head>
    <title>{title}</title>
    <style>
    </style>
  </head>
  <body>
    {body}
  </body>
</html>
'''


def html(body, title='no title'):
    return HTML.format(title=title, body=body)


if __name__ == '__main__':
    import os

    demo_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '..',
        'demo'
    )
    with open(os.path.join(demo_path, 'demo.txt')) as fp:
        lines = fp.readlines()

    with open(os.path.join(demo_path, 'demo.html'), 'w') as fp:
        fp.write(html(parser(lines)))
