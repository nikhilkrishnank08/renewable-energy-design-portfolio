# Solar PV Sizing Tool

Estimates installed capacity, annual generation, and SEAI grant entitlement
for domestic solar PV in Ireland.

## Inputs

- Roof area (m²), orientation, tilt angle, shading factor
- Panel specification (default: 440 W, ~1.95 m²)

## Methodology

System size is derived from usable roof area (85% of gross, to allow for
edge zones and obstructions) divided by panel area, then multiplied by
rated wattage.

Annual generation:

    E = kWp × I_base × f_orient × f_tilt × f_shade × η_system

Where `I_base` = 1050 kWh/m²/yr (south, 35° tilt, Irish average per PVGIS),
`η_system` = 0.85 (inverter, cabling, soiling losses).

## SEAI grant estimation

Grant is tiered: €700/kWp for the first 2 kWp, €200/kWp for the next 2 kWp,
capped at €1,800. The exact rates should always be verified against the
current SEAI scheme rules before quotation.

## Limitations

- Uses orientation/tilt lookup tables rather than PVGIS API; for quotation
  work, validate against PVGIS or an irradiance modelling tool.
- Self-consumption estimates are rules-of-thumb; actual figures depend on
  household demand profile and battery storage.