"""Regression tests pinning the published Avonside numbers."""
import numpy as np, pandas as pd, pathlib, pytest
from pylandstore import (wedge_volume, depth_for_volume, area_per_volume,
                         priestley_taylor_open_water, annual_loss_fraction,
                         lift_energy, solar_yield, backwater_wedge)

HERE = pathlib.Path(__file__).parent


def test_area_per_volume_depends_only_on_depth():
    for h in (1.0, 2.0, 3.5):
        assert area_per_volume(h, "wedge") == pytest.approx(2 / h)
        assert area_per_volume(h, "slot") == pytest.approx(1 / h)
    # identical across grades: A/V is grade-free by construction
    for g in (0.052, 0.40):
        h = depth_for_volume(50.0, g, 5.0)
        A = 5.0 * h / g
        assert A / 50.0 == pytest.approx(2 / h, rel=1e-9)


def test_steep_ground_forces_depth():
    """50 m3 in a 5 m width: 1.02 m on the bench, 2.83 m on the staircase."""
    assert depth_for_volume(50.0, 0.052, 5.0) == pytest.approx(1.02, abs=0.01)
    assert depth_for_volume(50.0, 0.40, 5.0) == pytest.approx(2.83, abs=0.01)
    assert wedge_volume(2.83, 0.40, 5.0) == pytest.approx(50.0, rel=0.01)


def test_open_water_evaporation_and_loss():
    """1260 mm/yr from 7424 MJ/m2/yr; 247% loss for a 1.02 m bench wedge."""
    E = priestley_taylor_open_water(7424.0)
    assert E == pytest.approx(1260.0, abs=5.0)
    assert annual_loss_fraction(1.02, E, "wedge") == pytest.approx(2.47, abs=0.03)
    assert annual_loss_fraction(2.83, E, "wedge") == pytest.approx(0.89, abs=0.03)
    assert annual_loss_fraction(3.0, E, "slot") == pytest.approx(0.42, abs=0.02)


def test_pumping_energy_and_solar():
    assert lift_energy(196.7) == pytest.approx(1.072, abs=0.002)
    assert lift_energy(163.7) == pytest.approx(0.892, abs=0.002)
    assert solar_yield(20.3) == pytest.approx(5.6, abs=0.15)
    assert solar_yield(8.4) == pytest.approx(2.3, abs=0.10)


def test_staircase_table_matches_published():
    t = pd.read_csv(HERE / "staircase_steps.csv")
    row = t[t.wall_h_m == 3.0].iloc[0]
    assert row.volume_m3 == pytest.approx(56.2, abs=0.2)
    assert int(row.n) == 28
    assert row.total_m3 == pytest.approx(1575, abs=2)


def test_backwater_is_positive_everywhere():
    """The grade-division form produced zero lengths; integration must not."""
    w = pd.read_csv(HERE / "jacobs_creek_weirs.csv")
    assert (w.backwater_len_m > 0).all()
    assert (w.storage_m3_per_m_width < 100).all()
    assert len(w) == 19


def test_backwater_on_a_flat_bed_is_finite():
    dist = np.arange(0, 100.0, 5.0)
    z = np.full_like(dist, 100.0); z[-1] = 99.5          # one tiny step
    area, length = backwater_wedge(dist, z, len(z) - 1, 0.5)
    assert np.isfinite(area) and np.isfinite(length) and length > 0
