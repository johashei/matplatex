"""matplatex: export matplotlib figures as pdf and text separately for
use in LaTeX.

Copyright (C) 2024 Johannes Sørby Heines

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys

from .__about__ import __version__
from .string_replacements import invalid_latex


class LaTeXinput:
    """Text to be input into a LaTeX document to include a figure.

    Instance variables:
    latexcode       The text in question as a string.
    graphic_isopen   Tracks whether a figure environment is currently
                    open in latexcode.
    widthcommand    The LaTeX length command which will be used to
                    define the width of the figure.

    Public methods:
    __init__            Constructor.
    includegraphics     Open a figure environment and include a figure.
    add_text            Draw a text box.
    endgraphics         Close a figure environment.
    addline             Add a single line of code to latexcode.
    write               Write latexcode to a file.
    """

    # only works for single characters
    # translatex = str.maketrans(invalid_latex)

    def __init__(self, *, widthcommand: str, externalize: bool):
        """Constructor for the LaTeXinput class.

        Keyword only arguments:
        widthcommand    The LaTeX length command which will be used to
                        define the width of the figure.
        externalize     Whether to use tikz externalize
        """
        self.graphic_isopen = False
        self.widthcommand = as_latex_command(widthcommand)
        self.externalize = externalize

        self.latexcode = '\n'.join([
            f"% This file was automatically generated by matpLaTeX {__version__}.",
            "% The source code is at https://github.com/johashei/matplatex.",
            "%",
            "% Requires package tikz.",
            "%",
            "% Usage:",
            "%",
            "In the preamble, add",
            rf"%   \newlength{{{self.widthcommand}}}",
            r"%   \newlength{\matplatextmp}",
            "%"
            "% Set the desired with of the figure using",
            rf"%   \setlength{{{self.widthcommand}}}{{<your desired width>}}",
            "%",
            "% Include the figure with",
            rf"%   \input{{<file name>.pdf_tex}}",
            "% or using the import package:",
            rf"%   \import{{<path>}}{{<file name>.pdf_tex}}",
            "%",
            "%"
            ])

    def includegraphics(self, graphics_filename, height_to_width: float):
        """ Start a tikzpicture and include the graphics."""
        if self.graphic_isopen:
            self.endgraphics()
        self.addline('')
        if self.externalize:
            self.addline(rf"\beginpgfgraphicnamed{{{graphics_filename}_xt}}")
            self.addline(r"\newlength{\matplatextmp}")
        self.latexcode += '\n'.join([
            r"\begingroup",
            "",
            rf"\setlength{{\matplatextmp}}{{{height_to_width}{self.widthcommand}}}",
            r"\hspace{-\parindent}",
            rf"\begin{{tikzpicture}}[x={self.widthcommand}, y=\matplatextmp]",
            rf"  \node[inner sep=0pt, above right] (graphics) at (0,0) {{",
            rf"    \includegraphics[width={self.widthcommand}]{{{graphics_filename}}}}};",
            ])
        self.graphic_isopen = True

    def add_text(self, text, position, *,
                 rotation=0, color=(0, 0, 0), alpha=1, anchor='center'):
        if len(color)==4:
            alpha = color[3]
        self.addline(rf"  \node [inner sep=0pt, "
                     rf"text={{rgb,1:red,{color[0]}; "
                                  rf"green,{color[1]}; "
                                  rf"blue,{color[2]}}}, "
                     rf"rotate={rotation}, "
                     rf"anchor={anchor}, "
                     rf"opacity={alpha}] "
                     rf"at ({position[0]}, {position[1]}) "
                     rf"{{{text}}};")

    def endgraphics(self):
        self.addline(r"\end{tikzpicture}")
        self.addline(r"\endgroup")
        if self.externalize:
            self.addline(r"\endpgfgraphicnamed")
        self.graphic_isopen = False

    def addline(self, text):
        self.latexcode += f"\n{text}"

    def write(self, filename):
        if self.graphic_isopen:
            self.endgraphics()
#        self.addline(rf"\global\let{self.widthcommand}\undefined%")
#        self.latexcode.replace('  ', '\t')
        self.latexcode = replace_multiple(self.latexcode, invalid_latex)
        with open(filename, 'w') as outfile:
            outfile.write(self.latexcode)


def as_latex_command(string: str, /):
    """Make sure the string begins with exactly one backslash."""
    return '\\' + string.strip('\\')

def replace_multiple(string: str, replacements: dict) -> str:
    for key, val in replacements.items():
        string = string.replace(key, val)
    return string

def trim(string):
    """Trim a multiline string.

    Docstring processing algorithm as implemented in PEP 257.
    """
    if not string:
        return ''
    lines = string.expandtabs().splitlines()
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    return '\n'.join(trimmed)
