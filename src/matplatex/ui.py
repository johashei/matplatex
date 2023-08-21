from beartype import beartype
import matplotlib.pyplot as plt

from .tools import write_tex, make_all_transparent, restore_colors
from .latex_input import LaTeXinput

@beartype
def save(figure: plt.Figure, filename: str):
    figure.draw_without_rendering() # Must draw text before it can be extracted.
    output = LaTeXinput()
    write_tex(output, figure, graphics=filename)
    output.write(f"{filename}.pdf_tex")
    color_backup = make_all_transparent(figure)
    figure.savefig(f"{filename}.pdf", format='pdf')
    restore_colors(figure, color_backup)
