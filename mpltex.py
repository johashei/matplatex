from functools import cached_property
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
from beartype import beartype

from LaTeXinput import LaTeXinput

@beartype
def save(fig: plt.Figure, /, filename: str):
    fig.draw_without_rendering() # Must draw text before it can be extracted.
    output = LaTeXinput()
    write_tex(output, fig, graphics=filename)
    output.write(f"{filename}.pdf_tex")
    color_backup = make_all_transparent(fig)
    fig.savefig(f"{filename}.pdf", format='pdf')
    restore_colors(fig, color_backup)

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


class FigureText:
    """Contain text and its tikz properties."""
    def __init__(
            self,
            text: mpl.text.Text,
            fig: plt.Figure,
            ax: plt.Axes | None = None):
        """Constructor for the FigureText class."""
        self._mpl_text = text
        self._figure_transform = fig.transFigure
        self._ax = ax

    @property
    def text(self):
        return self._mpl_text.get_text()

    @property
    def rotation(self):
        return self._mpl_text.get_rotation()

    @cached_property
    def position_in_figure(self):
        display_xy = self._mpl_text.get_transform().transform(
            self._mpl_text.get_position())
        figure_xy = self.figure_transform.inverted().transform(display_xy)
        return figure_xy

    @cached_property
    def tikz_anchor(self):
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
        anchor = (f"{anchor_by_va[self._mpl_text.get_va()]} "
                  f"{anchor_by_ha[self._mpl_text.get_ha()]}")
        if anchor == '':
            anchor = 'center'
        return anchor

    @cached_property
    def visible(self):
        if not self._mpl_text.get_visible():
            return False
        elif self._ax is None or not self._mpl_text.get_clip_on():
            return True
        else:
            return self._is_inside_ax()

    def _is_inside_ax(self):
        x, y = self._mpl_text.get_position()
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        if (xmin < x < xmax) and (ymin < y < ymax):
            return True
        else:
            return False


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

def draw_anchors(fig, figure_xy):
    ax = fig.get_children()[1]
    ax.plot(figure_xy[0], figure_xy[1], '+r', clip_on=False, transform=fig.transFigure,
            zorder=20)


