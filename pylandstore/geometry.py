"""Closed-form geometry for water held against a slope."""
from __future__ import annotations
import numpy as np


def wedge_volume(depth, grade, width):
    """Volume behind a wall of height `depth` on uniform `grade` (fraction)."""
    return np.asarray(width) * np.asarray(depth) ** 2 / (2 * np.asarray(grade))


def wedge_area(depth, grade, width):
    """Water-surface area of that wedge."""
    return np.asarray(width) * np.asarray(depth) / np.asarray(grade)


def depth_for_volume(volume, grade, width):
    """Wall height needed for `volume` at a given grade and width."""
    return np.sqrt(2 * np.asarray(grade) * np.asarray(volume) / np.asarray(width))


def area_per_volume(depth, shape="wedge"):
    """Water surface per cubic metre stored. Independent of grade.

    wedge (sloping floor): 2/h, mean depth h/2
    slot  (vertical sides): 1/h, mean depth h
    """
    h = np.asarray(depth, float)
    return (2.0 / h) if shape == "wedge" else (1.0 / h)
