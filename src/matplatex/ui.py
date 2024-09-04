from beartype import beartype
import matplotlib.pyplot as plt

from .tools import write_tex, make_all_transparent, restore_colors
from .latex_input import LaTeXinput

@beartype
def save(
        figure: plt.Figure,
        filename: str,
        *,
        widthcommand: str = r"\figurewidth",
        draw_anchors: bool = False,
        verbose: bool = True
        ):
    """Save matplotlib Figure with text in a separate tex file.

    Arguments:
    figure      The matplotlib Figure to save
    filename    The name to use for the files, without extention

    Optional keyword arguments:
    widthcommand    The LaTeX length command which will be used to
                    define the width of the figure.
    draw_anchors    If True, mark the text anchors on the figure.
                    Useful for debugging.
    verbose: bool   Print save message.
    """
    figure.draw_without_rendering() # Must draw text before it can be extracted.
    output = LaTeXinput(widthcommand=widthcommand)
    write_tex(output, figure, graphics=filename, add_anchors=draw_anchors)
    output.write(f"{filename}.pdf_tex")
    color_backup = make_all_transparent(figure)
    figure.savefig(f"{filename}.pdf", format='pdf')
    restore_colors(figure, color_backup)
    if verbose:
        print(f"Figure written to files {filename}.pdf_tex and {filename}.pdf")
