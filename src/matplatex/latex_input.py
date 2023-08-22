import sys

def as_latex_command(string: str, /):
    return '\\' + string.strip('\\')

class LaTeXinput:

    translatex = str.maketrans('\N{MINUS SIGN}', '-')

    def __init__(self, *, boxname: str, widthcommand: str):
        """Constructor for the LaTeXinput class.

        Keyword only arguments:
        boxname -- name of the box defined in the LaTeX preamble which
            will be used to size the figure.
        widthcommand -- the LaTeX length command which will be used to
            define the width of the figure.
        """
        self.open_graphics = False
        self.boxname = as_latex_command(boxname)
        self.widthcommand = as_latex_command(widthcommand)

        self.latexcode = trim(
            rf"""% This file was automatically generated by mpltex v0.0.4.
            % It most likely doesn't work yet.
            %
            % Usage:
            % Add "\newsavebox{self.boxname}" to your preamble, then include
            % the figure with
            %
            % \input{{<file name>.pdf_tex}}
            %
            % To scale the figure, write
            %
            % \def{self.widthcommand}{{<your desired width>}}
            % \input{{<file name>.pdf_tex}}
            %
            """)

    def includegraphics(self, graphics_filename):
        """ Start a tikzpicture and include the graphics."""
        if self.open_graphics:
            self.endgraphics()
        self.addline('')
        self.latexcode += trim(
             rf"""\begingroup

            \ifx{self.widthcommand}\undefined%
              \savebox{{{self.boxname}}}{{
                \includegraphics[scale=1]{{{graphics_filename}}}
                }}
            \else%
              \sbox{{{self.boxname}}}{{
                \includegraphics[width={self.widthcommand}]{{{graphics_filename}}}
                }}
            \fi%
            \def\unitwidth{{{self.widthcommand}}}
            \def\unitheight{{\ht{self.boxname}}}

            \hspace{{-\parindent}}
            \begin{{tikzpicture}}[x=\unitwidth, y=\unitheight]
              \node[inner sep=0pt, above right] (graphics) at (0,0) {{
                \includegraphics[width=\unitwidth]{{{graphics_filename}}}}};
            """)
        self.open_graphics = True

    def add_text(self, text, position, *,
                 alignment='', rotation=0, color='black', anchor='center'):
        self.addline(rf"  \node [inner sep=0pt, {alignment}, {color}, "
                     rf"rotate={rotation}, "
                     rf"anchor={anchor}] "
                     rf"at ({position[0]}, {position[1]}) "
                     rf"{{{text}}};")

    def endgraphics(self):
        self.addline(r"\end{tikzpicture}")
        self.addline(r"\endgroup")
        self.open_graphics = False

    def write(self, filename):
        if self.open_graphics:
            self.endgraphics()
        self.addline(rf"\global\let{self.widthcommand}\undefined%")
        self.latexcode.replace('  ', '\t')
        with open(filename, 'w') as outfile:
            outfile.write(self.latexcode.translate(self.translatex))

    def addline(self, text):
        self.latexcode += f"\n{text}"


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
