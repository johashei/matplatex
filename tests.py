import pytest
import mpltex

import matplotlib.pyplot as plt

@pytest.fixture
def make_simple_figure():
    """Make a figure with a single subplot and unique text objects."""
    fig, ax = plt.subplots()
    ax.plot([0,1], [0,2])
    ax.set_xlabel("x axis label")
    ax.set_ylabel("y axis label")
    ax.set_title("axis title")
    ax.set_xticks([0, 1, 2], ['none', 'I', 'II'])
    ax.set_yticks([0, 1/3, 2/3, 1], ['0', '1/3', '2/3', '1'])
    visible_text_objects = set(
        [ax.title, ax.xaxis.label, ax.yaxis.label]
        + ax.get_xticklabels()
        + ax.get_yticklabels()
        )
    return fig, visible_text_objects

def test_get_text(make_simple_figure):
    result = mpltex.extract_text(make_simple_figure[0])
    expected = make_simple_figure[1]
    assert result == expected

def test_make_all_transparent(make_simple_figure):
    mpltex.make_all_transparent(make_simple_figure[0])
    assert mpltex.extract_text(make_simple_figure[0]) == set()

def test_restore_colors(make_simple_figure):
    initial_state = mpltex.extract_text(make_simple_figure[0])
    removed_colors = mpltex.make_all_transparent(make_simple_figure[0])
    mpltex.restore_colors(make_simple_figure[0], removed_colors)
    final_state = mpltex.extract_text(make_simple_figure[0])
    assert initial_state == final_state

@pytest.fixture
def text_only_figure():
    text_coordinates = [(0.42, 0.2845), (0.2, 0.3), (0.8, 0.6)]
    fig = plt.Figure()
    ax = fig.add_axes((0.1, 0.1, 0.4, 0.4))
    fig.add_artist(plt.Text(*text_coordinates[0], 'text without axes'))
    ax.add_artist(plt.Text(*text_coordinates[1], 'ax text inside axes'))
    ax.add_artist(plt.Text(*text_coordinates[2], 'ax text outside axes'))
    return (fig, text_coordinates)

def test_get_position_in_figure(text_only_figure):
    result = []
    for text in mpltex.extract_text(text_only_figure[0]):
        result.append(text.get_position_in_figure)
    expected = text_only_figure[1]
    assert result == expected

def test_is_inside_ax(text_only_figure):
    _, text_inside, text_outside = mpltex.extract_text(text_only_figure[0])
    assert text_inside._is_inside_ax() == True
    assert text_outside._is_inside_ax() == False
