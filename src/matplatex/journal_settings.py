"""Predefined matplotlib size settings for journals.
"""
from attrs import define

_inches_per_mm = 0.03937

@define
class epj:
    column_width = 88 * _inches_per_mm
    full_width = 180 * _inches_per_mm
    font_size = 10

@define
class prc:
    column_width = 3.36
    full_width = 6.75
    font_size = 10
