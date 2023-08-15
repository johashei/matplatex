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
        draw_anchors(fig, element.get_position_in_figure()) # useful for checking positioning
        output.add_text(
            element.get_text(),
            position=element.get_position_in_figure(),
            anchor=element.get_tikz_anchor(),
            rotation=element.get_rotation())


class FigureText:
    """Contain text and its tikz properties."""
    def __init__(
            self,
            text: mpl.text.Text,
            fig: plt.Figure,
            ax: plt.Axes | None):
        """Constructor for the FigureText class."""
        self._mpl_text = text
        self._figure_transform = fig.transFigure
        self._ax = ax

    # I use getters and setters because the code behind them can be
    # complicated, take time, or fail. These are thing a user probably
    # doesn't extect attribute assignments to do. I may change my mind
    # about this in the future.

    def __str__(self):
        return (
            f"FigureText({self._mpl_text}, position={self._figure_xy}, "
            f"visible={self._visible}, tikz_anchor={self._tikz_anchor})")

    def get_text(self):
        return self._mpl_text.get_text()

    def get_tikz_anchor(self):
        return self._tikz_anchor

    def get_position_in_figure(self):
        return self._figure_xy

    def get_rotation(self):
        return self._mpl_text.get_rotation()

    def get_visible(self):
        return self._visible

    def get_color(self):
        return self._mpl_text.get_color()

    def set_color(self, value, /):
        self._mpl_text.set_color(value)

    @cached_property
    def _display_xy(self):
        return self._mpl_text.get_transform().transform(
            self._mpl_text.get_position())

    @cached_property
    def _figure_xy(self):
        return self._figure_transform.inverted().transform(self._display_xy)

    @cached_property
    def _axes_xy(self):
        if self._ax is None:
            raise ValueError("This text does not belong to any Axes")
        return self._ax.transAxes.inverted().transform(self._display_xy)

    @cached_property
    def _tikz_anchor(self):
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
    def _visible(self):
        if not self._mpl_text.get_visible():
            return False
        elif self._ax is None or not self._mpl_text.get_clip_on():
            return True
        else:
            return self._is_inside_ax()

    def _is_inside_ax(self):
        x, y = self._axes_xy
        if (0 <= x <= 1) or (0 <= y <= 1):
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
        removed_colors[text._mpl_text] = text.get_color()
        text.set_color("none")  # avoids messing with the whitespace
    return removed_colors

@beartype
def restore_colors(fig: plt.Figure, colors: dict):
    for text in get_text_decendents(fig):
        text.set_color(colors[text._mpl_text])

@beartype
def get_text_decendents(fig: plt.Figure, /):
    stack = [iter(fig.get_children())]
    current_ax = None
    while stack:
        try:
            child = next(stack[-1])
            if isinstance(child, mpl.text.Text):
                yield FigureText(text=child, fig=fig, ax=current_ax)
            else:
                if isinstance(child, plt.Axes):
                    current_ax = child
                stack.append(iter(child.get_children()))
        except StopIteration:
            stack.pop()

def draw_anchors(fig, figure_xy):
    ax = fig.get_children()[1]
    ax.plot(figure_xy[0], figure_xy[1], '+r', clip_on=False, transform=fig.transFigure,
            zorder=20)

def print_family_tree(mpl_object):
    stack = [iter(mpl_object.get_children())]
    print(stack)
    indent = ""
    while stack:
        try:
            child = next(stack[-1])
            print(f"{indent}{child}")
            stack.append(iter(child.get_children()))
            indent = indent[:-2]
            indent += "  |- "
        except StopIteration:
            indent = indent[:-5]
            indent += "- "
            stack.pop()
