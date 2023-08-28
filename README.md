# MatpLaTeX

MatpLaTeX lets you save a matplotlib `Figure` as a combination of a pdf file containing the graphics and a tex file containing the text. With this, text in the figure will automatically use the typeface, size and other settings of the surrounding text.

## Installation


## Basic Usage

To save a `Figure`, simply use
```
matplatex.save(fig, "myfig")
```
this will create two files named `myfig.pdf` and `myfig.pdf_tex`.
Add
```
\newsavebox\figurebox
``` 
to your LaTeX preamble and include the figure in your document with
```
\def\figurewidth{<width>}}
\input{myfig.pdf_tex}
```

## More Options

If you've already defined the commands `\figurebox` or `\figurewidth` as something else in your LaTeX document, you can change them to something else by passing the keyword arguments 'boxname' or 'widthcommand' to `matplatex.save`.

## Motivation

