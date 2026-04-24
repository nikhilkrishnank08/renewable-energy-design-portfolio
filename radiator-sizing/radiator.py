"""
Radiator sizing tool for low-temperature heat pump systems.

Heat pumps operate most efficiently at flow temperatures of 35-45 C,
vs 70-80 C for gas/oil boilers. Existing radiators sized for high-temp
systems are often undersized at heat pump flow temperatures. This tool
applies the EN 442 correction factors to size radiators for the actual
flow temperature in use.
"""

# EN 442 rated output is at DeltaT = 50 K
# Correction factor at other DeltaT follows:
#   Q_actual = Q_rated * (DT_actual / 50) ^ n
# where n ~ 1.3 for panel radiators

RADIATOR_EXPONENT = 1.3


def correction_factor(flow_temp: float, return_temp: float, room_temp: float) -> float:
    """Multiplicative correction to apply to EN 442 rated output."""
    mean_water_temp = (flow_temp + return_temp) / 2
    delta_t = mean_water_temp - room_temp
    if delta_t <= 0:
        raise ValueError('Flow temperature must exceed room temperature.')
    return (delta_t / 50) ** RADIATOR_EXPONENT


def required_rated_output(room_heat_loss_w: float,
                          flow_temp: float,
                          return_temp: float,
                          room_temp: float) -> dict:
    cf = correction_factor(flow_temp, return_temp, room_temp)
    required_rated_w = room_heat_loss_w / cf
    return {
        'correction_factor': round(cf, 3),
        'required_rated_output_w': round(required_rated_w, 0),
        'actual_output_at_flow_w': room_heat_loss_w,
    }


if __name__ == '__main__':
    # Example comparison: same radiator at boiler vs heat pump flow temps
    heat_loss = 1500  # W for the room
    room_temp = 21

    print('=== RADIATOR SIZING COMPARISON ===')
    print(f'Room heat loss: {heat_loss} W at {room_temp} C\n')

    scenarios = [
        ('Gas boiler (75/65)', 75, 65),
        ('Hybrid (55/45)', 55, 45),
        ('Heat pump (50/40)', 50, 40),
        ('Heat pump (45/35)', 45, 35),
    ]

    for name, flow, ret in scenarios:
        result = required_rated_output(heat_loss, flow, ret, room_temp)
        print(f'{name}:')
        print(f'  Correction factor: {result["correction_factor"]}')
        print(f'  Required EN 442 rated output: {result["required_rated_output_w"]} W')
        print()

    print('Note: a radiator rated for 1500 W at 75/65 delivers only ~650 W')
    print('at 45/35 flow. Retrofitting to a heat pump usually means either')
    print('upsizing radiators or switching to UFH/fan coil emitters.')