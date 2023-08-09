import matplotlib as mpl
import matplotlib.pyplot as plt

from beartype import beartype

@beartype
def extract_text(fig: plt.Figure):
    return set([t for t in get_text_decendents(fig)
                if t.get_visible() and t.get_text() != ''])

@beartype
def get_text_decendents(artist: mpl.artist.Artist):
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
