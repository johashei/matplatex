# MatpLaTeX

MatpLaTeX lets you save a matplotlib `Figure` as a combination of a pdf file containing the graphics and a LaTeX file containing the text. With this, text in the figure will automatically use the typeface, size and other settings of the surrounding text.

## Installation

MatpLaTeX is on PyPI, simply
```
pip install matplatex
```

### Python requirements:
- python >= 3.10 (If someone asks I may add support for earlier versions.)
- matplotlib >= 3.5
- beartype

### LaTeX requirements:
- tikz
- graphicx

## Basic Usage

To save a figure, simply use
```
matplatex.save(fig, "myfig")
```
this will create two files named `myfig.pdf` and `myfig.pdf_tex`.

In your LaTeX preamble, add the following
```
\newlength{\figurewidth}
\newlength{\matplatextmp}
```
and include the figure as such:
```
\setlength{\figurewidth}{<your desired width>}
\input{myfig.pdf_tex}
```
LaTeX commands such as `\small` and `\textbf{}` will affect the text in the expected way.

## Options

See the docstring of `matplatex.save()` for information on optional arguments.
A proper documentation is coming eventually.
