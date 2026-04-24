"""
Domestic Heat Loss Calculator
Based on I.S. EN 12831 methodology
Author: Nikhil Krishnan Karthikeyan Nair
For use in heat pump sizing per SEAI Domestic Technical Standards
"""

import pandas as pd
from dataclasses import dataclass, field
from typing import List

# Irish design external temperature (Met Eireann, per SEAI guidance)
DESIGN_EXTERNAL_TEMP = -3.0  # degrees C

# Typical U-values (W/m2K) - TGD Part L 2022 reference values
U_VALUES_REFERENCE = {
    'wall_pre_1978': 2.1,
    'wall_1978_2002': 1.1,
    'wall_2002_2011': 0.55,
    'wall_post_2011': 0.21,
    'wall_nzeb': 0.18,
    'roof_uninsulated': 2.3,
    'roof_insulated_old': 0.4,
    'roof_modern': 0.16,
    'floor_uninsulated': 0.8,
    'floor_modern': 0.18,
    'window_single': 4.8,
    'window_double_old': 2.8,
    'window_double_modern': 1.4,
    'window_triple': 0.9,
    'door_timber': 3.0,
    'door_insulated': 1.4,
}

# Design internal temperatures per CIBSE / SEAI
ROOM_TEMPS = {
    'living_room': 21,
    'kitchen': 18,
    'bedroom': 18,
    'bathroom': 22,
    'hall': 18,
    'utility': 16,
    'ensuite': 22,
}


@dataclass
class BuildingElement:
    """A wall, window, door, roof or floor element."""
    name: str
    area: float          # m2
    u_value: float       # W/m2K
    temp_difference: float  # K (usually internal - external)

    @property
    def heat_loss(self) -> float:
        """Fabric heat loss in Watts."""
        return self.area * self.u_value * self.temp_difference


@dataclass
class Room:
    name: str
    floor_area: float           # m2
    ceiling_height: float       # m
    design_temp: float          # degrees C
    air_changes_per_hour: float # ACH
    elements: List[BuildingElement] = field(default_factory=list)

    @property
    def volume(self) -> float:
        return self.floor_area * self.ceiling_height

    @property
    def fabric_loss(self) -> float:
        return sum(e.heat_loss for e in self.elements)

    @property
    def ventilation_loss(self) -> float:
        """Ventilation heat loss in W.
        Formula: 0.33 * ACH * Volume * dT
        0.33 = specific heat capacity of air (Wh/m3K)
        """
        dT = self.design_temp - DESIGN_EXTERNAL_TEMP
        return 0.33 * self.air_changes_per_hour * self.volume * dT

    @property
    def total_loss(self) -> float:
        return self.fabric_loss + self.ventilation_loss


def size_heat_pump(total_loss_w: float, dhw_allowance_w: float = 1500) -> dict:
    """Recommend heat pump size. Adds DHW allowance and 10% safety margin."""
    design_load_kw = (total_loss_w + dhw_allowance_w) / 1000
    recommended_kw = design_load_kw * 1.10

    standard_sizes = [5, 6, 8, 9, 11, 12, 14, 16]
    selected = next((s for s in standard_sizes if s >= recommended_kw),
                    standard_sizes[-1])

    return {
        'design_load_kw': round(design_load_kw, 2),
        'recommended_with_margin_kw': round(recommended_kw, 2),
        'selected_unit_kw': selected,
    }


def build_example_dwelling() -> List[Room]:
    """
    Example: a typical 3-bed semi-detached in Cork,
    pre-2002 build with partial retrofit (cavity insulation, new windows).
    Total floor area ~110 m2.
    """
    dT_living = 21 - DESIGN_EXTERNAL_TEMP  # 24 K
    dT_bed = 18 - DESIGN_EXTERNAL_TEMP     # 21 K
    dT_bath = 22 - DESIGN_EXTERNAL_TEMP    # 25 K

    living = Room('Living Room', 22.0, 2.4, 21, 1.0, [
        BuildingElement('External wall', 12.0, 0.55, dT_living),
        BuildingElement('Window (double glazed)', 3.5, 1.4, dT_living),
        BuildingElement('Ground floor', 22.0, 0.45, dT_living),
    ])

    kitchen = Room('Kitchen', 14.0, 2.4, 18, 1.5, [
        BuildingElement('External wall', 8.0, 0.55, 21),
        BuildingElement('Window', 1.8, 1.4, 21),
        BuildingElement('External door', 1.8, 1.4, 21),
        BuildingElement('Ground floor', 14.0, 0.45, 21),
    ])

    hall = Room('Hall & Stairs', 10.0, 2.4, 18, 1.0, [
        BuildingElement('External wall', 4.0, 0.55, 21),
        BuildingElement('Front door', 2.0, 1.4, 21),
        BuildingElement('Ground floor', 5.0, 0.45, 21),
    ])

    bed1 = Room('Master Bedroom', 14.0, 2.4, 18, 1.0, [
        BuildingElement('External wall', 10.0, 0.55, 21),
        BuildingElement('Window', 2.0, 1.4, 21),
        BuildingElement('Roof', 14.0, 0.25, 21),
    ])

    bed2 = Room('Bedroom 2', 11.0, 2.4, 18, 1.0, [
        BuildingElement('External wall', 8.0, 0.55, 21),
        BuildingElement('Window', 1.8, 1.4, 21),
        BuildingElement('Roof', 11.0, 0.25, 21),
    ])

    bed3 = Room('Bedroom 3', 8.0, 2.4, 18, 1.0, [
        BuildingElement('External wall', 6.0, 0.55, 21),
        BuildingElement('Window', 1.2, 1.4, 21),
        BuildingElement('Roof', 8.0, 0.25, 21),
    ])

    bathroom = Room('Bathroom', 5.0, 2.4, 22, 2.0, [
        BuildingElement('External wall', 4.0, 0.55, dT_bath),
        BuildingElement('Window', 0.6, 1.4, dT_bath),
        BuildingElement('Roof', 5.0, 0.25, dT_bath),
    ])

    return [living, kitchen, hall, bed1, bed2, bed3, bathroom]


def produce_report(rooms: List[Room]) -> pd.DataFrame:
    rows = []
    for r in rooms:
        rows.append({
            'Room': r.name,
            'Area (m2)': r.floor_area,
            'Design Temp (C)': r.design_temp,
            'Fabric Loss (W)': round(r.fabric_loss, 0),
            'Ventilation Loss (W)': round(r.ventilation_loss, 0),
            'Total Loss (W)': round(r.total_loss, 0),
            'W per m2': round(r.total_loss / r.floor_area, 1),
        })
    df = pd.DataFrame(rows)
    total_row = pd.DataFrame([{
        'Room': 'TOTAL',
        'Area (m2)': df['Area (m2)'].sum(),
        'Design Temp (C)': '',
        'Fabric Loss (W)': df['Fabric Loss (W)'].sum(),
        'Ventilation Loss (W)': df['Ventilation Loss (W)'].sum(),
        'Total Loss (W)': df['Total Loss (W)'].sum(),
        'W per m2': round(df['Total Loss (W)'].sum() / df['Area (m2)'].sum(), 1),
    }])
    return pd.concat([df, total_row], ignore_index=True)


if __name__ == '__main__':
    rooms = build_example_dwelling()
    report = produce_report(rooms)

    print('\n=== HEAT LOSS CALCULATION REPORT ===')
    print(f'Design external temperature: {DESIGN_EXTERNAL_TEMP} C')
    print(f'Standard: I.S. EN 12831\n')
    print(report.to_string(index=False))

    total_loss_w = sum(r.total_loss for r in rooms)
    hp = size_heat_pump(total_loss_w)

    print(f'\n=== HEAT PUMP SIZING ===')
    print(f'Total building heat loss: {total_loss_w/1000:.2f} kW')
    print(f'Plus DHW allowance (1.5 kW): {hp["design_load_kw"]} kW')
    print(f'With 10% safety margin: {hp["recommended_with_margin_kw"]} kW')
    print(f'Recommended standard unit: {hp["selected_unit_kw"]} kW')

    report.to_excel('heat_loss_report.xlsx', index=False)
    print('\nReport exported to heat_loss_report.xlsx')