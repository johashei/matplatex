import pytest
import mpltex

import matplotlib.pyplot as plt

@pytest.fixture
def make_simple_figure():
    fig, ax = plt.subplots()
    ax.plot([0,1], [0,1])
    ax.set_xlabel("x axis label")
    ax.set_ylabel("y axis label")
    ax.set_title("axis title")
    return fig

def test_get_text(make_simple_figure):
    expected = set(("x axis label", "y axis label", "axis title"))
    result = mpltex.extract_text(make_simple_figure)
    assert result == expected
