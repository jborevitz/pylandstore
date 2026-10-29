"""Storage measured from a DEM, and weir siting along a profile."""
from __future__ import annotations
import numpy as np
from scipy import ndimage


def flood_storage(dem, row, col, water_level, catchment_mask):
    """Storage behind a dam at (row, col) with a level water surface.

    `catchment_mask` is mandatory and must come from an upstream delineation.
    Without it the fill escapes down-valley and the volume is meaningless --
    an unmasked run on a 47 ha farm returned 57 million cubic metres.
    """
    d = np.asarray(dem, float)
    reg = np.zeros(d.shape, bool); reg[row, col] = True
    k = np.ones((3, 3))
    prev = -1
    while reg.sum() != prev:
        prev = reg.sum()
        reg = ndimage.binary_dilation(reg, k) & (d < water_level) & catchment_mask
    storage = float(((water_level - d[reg])).sum())      # x cell area by caller
    perim = reg & ~ndimage.binary_erosion(reg, k)
    return reg, storage, perim


def backwater_wedge(dist, z, index, height):
    """Longitudinal wedge area and backwater length upstream of a crest.

    Integrated along the surveyed bed rather than divided by a local grade:
    the grade form divides by zero on flat cells and produced both zero-length
    backwaters and a 1250 m3 artefact before this was fixed.
    """
    zc = z[index] + height
    area = 0.0; length = 0.0
    j = index
    while j > 0:
        seg = dist[j] - dist[j-1]
        zu = z[j-1]
        if zu >= zc:
            f = (zc - z[j]) / max(zu - z[j], 1e-9)
            area += 0.5 * (zc - z[j]) * seg * f
            length += seg * f
            break
        area += 0.5 * ((zc - z[j]) + (zc - zu)) * seg
        length += seg
        j -= 1
    return area, length


def weir_sites(dist, z, height, start_m=0.0):
    """Place a weir each time the bed has fallen `height` since the last one."""
    out = []
    zref = None
    for i in range(len(z)):
        if dist[i] < start_m:
            continue
        if zref is None:
            zref = z[i]; continue
        if zref - z[i] >= height:
            area, length = backwater_wedge(dist, z, i, height)
            out.append(dict(index=i, dist_m=float(dist[i]), crest_elev_m=float(z[i]),
                            backwater_len_m=float(length), wedge_area_m2=float(area)))
            zref = z[i]
    return out
