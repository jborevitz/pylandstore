"""Water storage geometry on sloping land: weirs, ponds, tanks and the pump.

Three results shape this module.

1. Surface area per cubic metre depends only on DEPTH, not grade.  A wedge
   with a sloping floor gives A/V = 2/h; a vertical-sided slot gives 1/h.
   Evaporative loss follows directly, so depth is the design variable.
2. Grade still matters, because it fixes the depth you get for a given volume
   and width.  Steep ground therefore yields deep, low-evaporation stores and
   gentle ground yields shallow, lossy ones -- the opposite of the intuition
   that flat land is better for water.
3. Staging a pump up a hillside saves no energy.  Lift is rho*g*H whatever the
   number of stages; extra stages only add losses.  Stage for operational
   reasons (still-water intake, continuous running, mid-slope offtake).
"""
from .geometry import wedge_volume, wedge_area, area_per_volume, depth_for_volume
from .ponds import flood_storage, backwater_wedge, weir_sites
from .evaporation import priestley_taylor_open_water, annual_loss_fraction
from .pumping import lift_energy, solar_yield, fill_time

__all__ = ["wedge_volume","wedge_area","area_per_volume","depth_for_volume",
           "flood_storage","backwater_wedge","weir_sites",
           "priestley_taylor_open_water","annual_loss_fraction",
           "lift_energy","solar_yield","fill_time"]
__version__ = "0.1.0"
