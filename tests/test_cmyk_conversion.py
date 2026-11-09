from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import pytest

from matplatex.ui import save
from matplatex.extensions import convert2cmyk_gs

@pytest.fixture
def save_rgb_figure_pdf(tmp_path):
    savepath = tmp_path/'figure_rgb'
    fig, ax = plt.subplots()
    ax.axvspan(0, 1, color='g')
    gfx_path = save(fig, savepath)
    return gfx_path, savepath

def test_save_return(save_rgb_figure_pdf):
    result, savepath = save_rgb_figure_pdf
    expected = savepath.with_suffix('.gfx.pdf')
    assert result == expected

def test_cmyk_gs(save_rgb_figure_pdf, tmp_path):
    rgb_path, _ = save_rgb_figure_pdf
    cmyk_path = tmp_path/'figure_cmyk.pdf'
    convert2cmyk_gs(rgb_path, cmyk_path)
