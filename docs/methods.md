# pylandstore — methods

Conventions, traps and limitations. Findings from the block this was developed on are in the [README](../README.md).


## Three results worth knowing before you dig

**Surface area per cubic metre depends only on depth, not grade.** A wedge with a
sloping floor gives `A/V = 2/h`; a vertical-sided slot gives `1/h`. Evaporative loss
follows directly, so depth is the design variable and vertical sides are not a
refinement but the whole intervention.

**Grade still matters, because it fixes the depth you get.** 50 m³ in a 5 m width is
1.02 m deep on 5% ground and 2.83 m deep on 40% ground. Steep land therefore yields
deep, low-evaporation stores and gentle land yields shallow, lossy ones — the
opposite of the intuition that flat ground is better for water.

**Staging a pump up a hillside saves no energy.** Lift is ρgH whatever the number of
stages; extra stages only add losses. Stage for operational reasons — a still-water
intake, continuous running, a mid-slope offtake — not for efficiency.

## Two bugs this module exists to prevent

`flood_storage` **requires** a catchment mask. A dam impounds only its own catchment;
an unmasked flood-fill escapes down-valley. On a 47 ha farm the unmasked version
returned 57 million cubic metres.

`backwater_wedge` integrates the wedge along the surveyed bed instead of dividing by a
local grade. The division form hits zero grade on flat cells and produced both
zero-length backwaters and a 1250 m³ artefact.

## Evaporation numbers are modelled

`priestley_taylor_open_water` assumes `Rn = 0.60 Rs` and `Δ/(Δ+γ) = 0.55` near 10 °C.
Both are assumptions, not measurements. State them wherever the number is quoted.
