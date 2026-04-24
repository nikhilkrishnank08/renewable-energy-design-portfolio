# Radiator Sizing for Low-Temperature Heat Pump Systems

Resizes emitters from the traditional 75/65°C boiler flow regime to
low-temperature heat pump operation (typically 45/35°C or 50/40°C).

## Why this matters

EN 442 radiators are rated at ΔT = 50 K. Dropping the mean water
temperature reduces output roughly as:

    Q_actual = Q_rated × (ΔT_actual / 50) ^ 1.3

A radiator that delivers 1500 W at 75/65 flow delivers only ~650 W
at 45/35. Every heat pump retrofit needs this check on every emitter.

## Use

    py radiator.py

Compares the same room's required rated output at four common flow regimes.

## Integration

In a full retrofit design this tool pairs with the heat loss calculator:
room-by-room heat loss feeds directly into this sizing check to
determine which emitters need replacement or whether a switch to UFH
is warranted.