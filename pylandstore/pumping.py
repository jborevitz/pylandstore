"""Lift energy and solar sizing."""
from __future__ import annotations
import numpy as np

G = 9.81
J_PER_KWH = 3.6e6


def lift_energy(lift_m, system_efficiency=0.50):
    """kWh per cubic metre raised. Depends only on total lift, so staging a
    pump up a hill saves nothing -- each extra stage adds losses."""
    return G * np.asarray(lift_m) * 1000.0 / J_PER_KWH / system_efficiency


def solar_yield(shortwave_mj_per_day, module_efficiency=0.20):
    """kWh per day per kWp of array, from daily shortwave in MJ m-2 d-1.
    One kWp occupies 1/(module_efficiency) square metres at 1 kW m-2 STC."""
    area_per_kwp = 1.0 / module_efficiency
    return np.asarray(shortwave_mj_per_day) * area_per_kwp * module_efficiency / 3.6


def fill_time(volume_m3, lift_m, array_kwp, shortwave_mj_per_day, **kw):
    """Days to fill a store. Use winter shortwave to size for the lean season."""
    e = float(volume_m3) * lift_energy(lift_m, kw.get("system_efficiency", 0.50))
    return e / (array_kwp * solar_yield(shortwave_mj_per_day,
                                        kw.get("module_efficiency", 0.20)))
