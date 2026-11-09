"""matplatex.extensions: extentions to the matplatex tool.

Copyright (C) 2026 Johannes Sørby Heines

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pathlib import Path
import subprocess
import sys

def cmyk(graphics_path: Path, cleanup=True):
    """Convert generated graphics to the CMYK colour space.

    The converted file is saved with the same name as the give input.
    If cleanup is False, the original is saved as <name>.orginal_gfx.<ext>

    Arguments
    ---------
    graphics_path   Path to the graphics file.
    cleanup         Delete the original graphics file (default True).
    """
    gfx_stem = Path(graphics_path.stem)  # should be of the form name.gfx
    new_stem = gfx_stem.with_suffix('.original_gfx')  # name.original_gfx
    new_path = graphics_path.with_stem(new_stem.name)  # /path/name.original_gfx.ext
    path_to_original = graphics_path.rename(new_path)

    match graphics_path.suffix:
        case '.pdf':
            convert2cmyk_gs(path_to_original, graphics_path)
        case '_':
            raise RuntimeError(
                "Conversion to CMYK is only available for the following"
                " file types: pdf."
                )
    if cleanup:
        path_to_original.unlink()
        print("Original RGB graphics deleted.")
    else:
        print(f"Original RGB graphics saved as {path_to_original}", file=sys.stderr)

def convert2cmyk_gs(original: Path, new: Path):
    gs_convert = [
        'gs',
        '-o', f'{new}',
        '-sDEVICE=pdfwrite',
#        '-sProcessColorModel=DeviceCMYK',
        '-sColorConversionStrategy=CMYK',
        '-sColorConversionStrategyForImages=CMYK',
        f'{original}'
        ]
    try:
        gs = subprocess.run(gs_convert, capture_output=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        msg = (f"{e}\nError: {e.stderr}\nOutput: {e.stdout}")
        raise RuntimeError(msg) from e
    print(f"Converting graphics to CMYK\n{gs.stdout}", file=sys.stderr)


