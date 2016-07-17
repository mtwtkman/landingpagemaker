# What

This makes easily fucking ugly landing page called 'インターネット情報商材' in japanese.
You know, those are really ugly.

## Reserve keywords.

- `#`
- `*`
- `_`
- `-`
- `img`
- `|`
- `>`
- `<`

Those reserve keywords must be escaped when you want to treat literal character same as markdown. Like

`*\*foo*` converted to `<span style="font-weight:bold;">*foo</span>`


# Basic rules

## Header

`#foo` converted to `<h1>foo</h1>`
`##foo` converted to `<h2>foo</h2>`
... like markdown.

## Decotaion

`*foo*` converted to `<span style="font-weight:bold;">foo</span>`
`_foo_` converted to `<span style="text-decoration:underline;">foo</span>`
`img=src` converted to `<img src="src">`
`|foo|` converted to `<span style="background-color:yellow;">foo</span>`  default color is yeallow.

## Styles

### font
`<str>:color:size`

Only font size and color can be specified like

`*foo*:rgb(255,0,0):12pt` converted to `<span style="font-weight:bold;color:rgb(255,0,0);font-size:12pt;">foo</span>`

### image

You can specify size and align to `<img>`.

**Align Right**
Use `>` at front of `img` keyword.
`>img=src` converted to `<img src="src" align="right">`

**Align Left**
Use `<` at front of `img` keyword.
`<img=src` converted to `<img src="src" align="left">`

**Size**
Some ways.

`img=src:w20` converted to `<img src="src" width="20">`
`img=src:h20` converted to `<img src="src" height="20">`
`img=src:20x60` converted to `<img src="src" width="20" height="60">`

## Others

`-` converted to `<hr>`
All blanks which are both ends are ignored.
