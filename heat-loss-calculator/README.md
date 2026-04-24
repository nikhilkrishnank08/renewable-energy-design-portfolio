# Domestic Heat Loss Calculator

Room-by-room heat loss calculation tool for dwelling heat pump sizing,
implemented to I.S. EN 12831 methodology and aligned with SEAI Domestic
Technical Standards and TGD Part L 2022 reference U-values.

## Purpose

Undersized heat pumps fail to maintain comfort on design-day conditions;
oversized units short-cycle and run inefficiently. Accurate room-by-room
heat loss calculation is the foundation of a correctly sized low-temperature
heating system.

## Methodology

For each room:

- **Fabric loss**: Q = Σ (U × A × ΔT) across walls, roofs, floors, windows, doors
- **Ventilation loss**: Q = 0.33 × ACH × Volume × ΔT
- **Total room load** = fabric + ventilation

Design external temperature: -3°C (Met Éireann data, per SEAI guidance).
Internal temperatures: living 21°C, bedrooms 18°C, bathrooms 22°C (CIBSE).

Heat pump sizing adds an allowance for DHW (1.5 kW) and a 10% safety margin,
then selects the next standard unit size up.

## Running it

    py -m venv venv
    venv\Scripts\activate
    pip install pandas openpyxl
    py heat_loss.py

Outputs a console report and `heat_loss_report.xlsx`.

## Example output

Example dwelling: a 110 m² pre-2002 semi-detached with partial retrofit
(cavity insulation, double-glazed windows). Total calculated load ~6.8 kW,
sized to an 8 kW air-to-water unit.

## Limitations

- Uses reference U-values; a real survey requires measured or BER-assessed values.
- Thermal bridging factor not explicitly added (assume 10% uplift for older
  dwellings if not separately modelled).
- Does not model solar gains or internal gains (conservative for sizing).

## Regulatory context

- **SEAI**: Heat pump grant requires a Heat Loss Indicator ≤ 2.3 W/m²K and
  a BER of B2 or better. Sizing must follow the Domestic Technical Standards.
- **TGD Part L 2022**: Defines maximum U-values for new-build and major
  renovation.
- **I.S. EN 12831**: European standard for heating system design load.