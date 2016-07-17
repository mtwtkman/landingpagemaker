# -*- coding: utf-8 -*-
import os
import sys
import unittest


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)


from converter import parser


class Test(unittest.TestCase):
    def _callFUT(self, src):
        return parser(src)

    def test_header_with_blank_with_both_ends(self):
        src = '  #header   '
        result = self._callFUT(src)
        self.assertEqual(result, '<h1>header</h1>')

    def test_header1(self):
        src = '#header1'
        result = self._callFUT(src)
        self.assertEqual(result, '<h1>header1</h1>')

    def test_header2(self):
        src = '##header2'
        result = self._callFUT(src)
        self.assertEqual(result, '<h2>header2</h2>')

    def test_header3(self):
        src = '###header3'
        result = self._callFUT(src)
        self.assertEqual(result, '<h3>header3</h3>')

    def test_header_many(self):
        src = '#' * 7 + 'header_many'
        result = self._callFUT(src)
        self.assertEqual(result, '<h6>#header_many</h6>')

    def test_escaped_sharp(self):
        src = '\#normal'
        result = self._callFUT(src)
        self.assertEqual(result, '<span>#normal</span>')

    def test_header_has_escaped_sharp(self):
        src = '#\#hi'
        result = self._callFUT(src)
        self.assertEqual(result, '<h1>#hi</h1>')

    def test_bold(self):
        src = '*bold*'
        result = self._callFUT(src)
        self.assertEqual(result, '<span style="font-weight:bold;">bold</span>')

    def test_color_name(self):
        src = '*bold*:red'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="font-weight:bold;color:red;">'
                                  'bold</span>'))

    def test_color_rgb(self):
        src = '*bold*:rgb(1,255,99)'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="font-weight:bold;'
                                  'color:rgb(1,255,99);">bold</span>'))

    def test_color_hex3(self):
        src = '*bold*:#f29'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="font-weight:bold;'
                                  'color:#f29;">bold</span>'))

    def test_color_hex6(self):
        src = '*bold*:#fFab73'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="font-weight:bold;'
                                  'color:#fFab73;">bold</span>'))

    def test_underline(self):
        src = '_foo_'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="text-decoration:underline;">'
                                  'foo</span>'))

    def test_multiline(self):
        src = ['foo', '*bar*']
        result = self._callFUT(src)
        self.assertEqual(result, (
            '<span>foo</span>'
            '<p></p>'
            '<span style="font-weight:bold;">bar</span>')
        )

    def test_size_no_unit(self):
        src = '*foo*:12'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="font-weight:bold;'
                                  'font-size:12pt;">foo</span>'))

    def test_size_specified_pt_unit(self):
        src = '*foo*:12pt'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="font-weight:bold;'
                                  'font-size:12pt;">foo</span>'))

    def test_size_and_color(self):
        src = '*foo*:12:red'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="font-weight:bold;'
                                  'color:red;font-size:12pt;">foo</span>'))

    def test_color_and_size(self):
        src = '*foo*:red:12'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="font-weight:bold;'
                                  'color:red;font-size:12pt;">foo</span>'))

    def test_text_bg_color(self):
        src = '|foo|'
        result = self._callFUT(src)
        self.assertEqual(result, ('<span style="background-color:yellow;">'
                                  'foo</span>'))

    def test_horizon_separater(self):
        src = ['foo', '-', 'bar']
        result = self._callFUT(src)
        self.assertEqual(result, ('<span>foo</span><p></p>'
                                  '<hr><p></p><span>bar</span>'))

    def test_img(self):
        src = 'img=cat.png'
        result = self._callFUT(src)
        self.assertEqual(result, '<img src="cat.png">')

    def test_img_right(self):
        src = '>img=cat.png'
        result = self._callFUT(src)
        self.assertEqual(result, '<img src="cat.png" align="right">')

    def test_img_left(self):
        src = '<img=cat.png'
        result = self._callFUT(src)
        self.assertEqual(result, '<img src="cat.png" align="left">')

    def test_img_width(self):
        src = 'img=cat.png:w20'
        result = self._callFUT(src)
        self.assertEqual(result, '<img src="cat.png" width="20">')

    def test_img_height(self):
        src = 'img=cat.png:h20'
        result = self._callFUT(src)
        self.assertEqual(result, '<img src="cat.png" height="20">')

    def test_img_width_and_height(self):
        src = 'img=cat.png:20x60'
        result = self._callFUT(src)
        self.assertEqual(result, '<img src="cat.png" width="20" height="60">')


if __name__ == '__main__':
    unittest.main()
