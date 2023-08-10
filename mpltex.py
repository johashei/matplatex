import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
from beartype import beartype

from LaTeXinput import LaTeXinput

@beartype
def save(fig: plt.Figure, /, filename: str):
    mpl_text = extract_text(fig)
    print(mpl_text)
    colors = make_all_transparent(fig)
    fig.savefig(f"{filename}.pdf", format='pdf')
    restore_colors(fig, colors)
    output = LaTeXinput()
    write_tex(output, fig, graphics=filename)
    output.write(f"{filename}.pdf_tex")

def write_tex(output: LaTeXinput, fig, *, graphics):
    output.includegraphics(graphics)
    for element in extract_text(fig):
        xy = get_position_in_figure(fig, element)
        letters = element.get_text()
        alignment = get_tikz_alignment(element)
        output.add_text(letters, xy, alignment)

def get_position_in_figure(fig, mpl_text: mpl.text.Text):
    display_xy = mpl_text.get_transform().transform(mpl_text.get_position())
    figure_xy = fig.transFigure.inverted().transform(display_xy)
    return figure_xy

def get_tikz_alignment(mpl_text):
    mpl2tikz = {'bottom':'above', 'top':'below',
                'right':'left', 'left':'right',
                'center':'', 'baseline':'', 'center_baseline':''}
    return f"{mpl2tikz[mpl_text.get_va()]} {mpl2tikz[mpl_text.get_ha()]}"

@beartype
def extract_text(fig: plt.Figure, /):
    return remove_transparent(remove_empty(remove_invisible(
        set(get_text_decendents(fig)))))

def remove_invisible(text_set: set, /):
    return {element for element in text_set if element.get_visible()}

def remove_empty(text_set: set, /):
    return {element for element in text_set if element.get_text() != ''}

def remove_transparent(text_set: set, /):
    return {element for element in text_set if element.get_color() != 'none'}

@beartype
def make_all_transparent(fig: plt.Figure, /):
    removed_colors = {}
    for text in get_text_decendents(fig):
        removed_colors[text] = text.get_color()
        text.set_color("none")  # avoids messing with the whitespace
    print(removed_colors)
    return removed_colors

@beartype
def restore_colors(fig: plt.Figure, /, colors: dict):
    pass
    for text in get_text_decendents(fig):
        text.set_color(colors[text])

@beartype
def get_text_decendents(artist: mpl.artist.Artist, /):
    stack = [iter(artist.get_children())]
    while stack:
        try:
            child = next(stack[-1])
            if isinstance(child, mpl.text.Text):
                yield child
            else:
                stack.append(iter(child.get_children()))
        except StopIteration:
            stack.pop()


