import matplotlib as mpl
import matplotlib.pyplot as plt

from beartype import beartype

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

def make_all_transparent(fig: plt.Figure, /):
    for text in get_text_decendents(fig):
        text.set_color("none")


@beartype
def get_text_decendents(artist: mpl.artist.Artist, /):
    stack = [iter(artist.get_children())]
    print(stack)
    while stack:
        try:
            child = next(stack[-1])
            #print(child)
            if isinstance(child, mpl.text.Text):
                yield child
            else:
                stack.append(iter(child.get_children()))
        except StopIteration:
            stack.pop()
