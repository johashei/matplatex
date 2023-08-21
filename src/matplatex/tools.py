import matplotlib.pyplot as plt
from beartype import beartype

from .latex_input import LaTeXinput

def write_tex(output: LaTeXinput, fig, *, graphics):
    output.includegraphics(graphics)
    for element in extract_text(fig):
        xy = get_position_in_figure(fig, element)
        draw_anchors(fig, xy) # useful for checking positioning
        output.add_text(
            element.get_text(),
            position=xy,
            anchor=get_tikz_anchor(element),
            rotation=element.get_rotation())

def get_position_in_figure(fig, mpl_text: plt.Text):
    display_xy = mpl_text.get_transform().transform(mpl_text.get_position())
    figure_xy = fig.transFigure.inverted().transform(display_xy)
    return figure_xy

def get_tikz_anchor(mpl_text):
    anchor_by_va = {
        'bottom': 'south',
        'top': 'north',
        'center': '',
        'baseline': 'base',
        'center_baseline': 'mid'
        }
    anchor_by_ha = {
        'right': 'east',
        'left': 'west',
        'center': ''
        }
    anchor = (f"{anchor_by_va[mpl_text.get_va()]} "
              f"{anchor_by_ha[mpl_text.get_ha()]}")
    if anchor == '':
        anchor = 'center'
    return anchor

def determine_positioning(fig, mpl_text):
    fig.draw_without_renderning()
    mpl_text.get_window_extent()
    return


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
    return removed_colors

@beartype
def restore_colors(fig: plt.Figure, colors: dict):
    pass
    for text in get_text_decendents(fig):
        text.set_color(colors[text])

@beartype
def get_text_decendents(artist: plt.Artist, /):
    stack = [iter(artist.get_children())]
    while stack:
        try:
            child = next(stack[-1])
            if isinstance(child, plt.Text):
                yield child
            else:
                stack.append(iter(child.get_children()))
        except StopIteration:
            stack.pop()

def draw_anchors(fig, figure_xy):
    ax = fig.get_children()[1]
    ax.plot(figure_xy[0], figure_xy[1], '+r', clip_on=False,
            transform=fig.transFigure, zorder=20)


