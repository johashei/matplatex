from beartype import beartype
import matplotlib.pyplot as plt

from .tools import write_tex, make_all_transparent, restore_colors
from .latex_input import LaTeXinput

@beartype
def save(figure: plt.Figure, filename: str, *,
         boxname: str = r"\figurebox", widthcommand: str = r"\figurewidth",
         draw_anchors=False):
    """Save matplotlib Figure with text in a separate tex file.

    Arguments:
    figure -- the matplotlib Figure to save
    filename -- the name to use for the files, without extention

    Optional keyword arguments (passed to LaTeXinput):
    boxname -- name of the box defined in the LaTeX preamble which will
        be used to size the figure.
    widthcommand -- the LaTeX length command which will be used to
        define the width of the figure.
    draw_anchors -- whether to mark the text anchors on the figure. Useful for
        debugging. Default False.
    """
    figure.draw_without_rendering() # Must draw text before it can be extracted.
    output = LaTeXinput(boxname=boxname, widthcommand=widthcommand)
    write_tex(output, figure, graphics=filename, add_anchors=draw_anchors)
    output.write(f"{filename}.pdf_tex")
    color_backup = make_all_transparent(figure)
    figure.savefig(f"{filename}.pdf", format='pdf')
    restore_colors(figure, color_backup)
