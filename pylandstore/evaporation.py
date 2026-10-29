"""Open-water evaporation and what it costs a small store."""
from __future__ import annotations
import numpy as np

LAMBDA_MJ_PER_KG = 2.45
ALPHA_PT = 1.26
WATER_ALBEDO = 0.06


def priestley_taylor_open_water(shortwave_mj, rn_fraction=0.60, delta_ratio=0.55,
                                alpha=ALPHA_PT):
    """Open-water evaporation in mm, from incoming shortwave in MJ m-2.

    `delta_ratio` is Delta/(Delta+gamma), about 0.55 near 10 C.  `rn_fraction`
    approximates net/incoming radiation for water over a year.  Both are
    assumptions, not measurements: state them wherever the number is quoted.
    """
    return alpha * delta_ratio * (rn_fraction * np.asarray(shortwave_mj)) / LAMBDA_MJ_PER_KG


def annual_loss_fraction(depth, evaporation_mm, shape="wedge"):
    """Annual evaporative loss as a fraction of the stored volume."""
    from .geometry import area_per_volume
    return area_per_volume(depth, shape) * np.asarray(evaporation_mm) / 1000.0
