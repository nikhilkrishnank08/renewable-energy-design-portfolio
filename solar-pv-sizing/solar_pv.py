"""
Solar PV System Sizing Tool - Irish domestic installations.
Considers SEAI grant structure, roof orientation, shading, and
typical Irish irradiance.
"""

from dataclasses import dataclass

# Average annual irradiance on a south-facing surface at 35 deg tilt
# in Ireland, per SEAI/PVGIS: ~1050 kWh/m2/yr
BASE_IRRADIANCE_KWH_M2 = 1050

# Orientation correction factors (relative to south-facing optimal)
ORIENTATION_FACTORS = {
    'south': 1.00,
    'south_east': 0.96,
    'south_west': 0.96,
    'east': 0.85,
    'west': 0.85,
    'north_east': 0.70,
    'north_west': 0.70,
    'north': 0.60,
}

# Tilt correction relative to 35 deg
TILT_FACTORS = {
    0: 0.88,    # flat
    15: 0.94,
    25: 0.98,
    35: 1.00,
    45: 0.98,
    60: 0.91,
}

# SEAI grant (as of scheme guidelines - always verify against current rates)
SEAI_GRANT_STRUCTURE = [
    (0, 2, 700),    # up to 2 kWp: 700 per kWp
    (2, 4, 200),    # 2-4 kWp additional: 200 per kWp
]
SEAI_GRANT_CAP = 1800


@dataclass
class PVSystem:
    roof_area_m2: float
    orientation: str
    tilt_degrees: int
    shading_factor: float = 1.0  # 1.0 = no shading, 0.8 = 20% shaded
    panel_wattage: int = 440     # typical modern panel
    panel_area_m2: float = 1.95  # typical ~2 m2 per panel
    system_losses: float = 0.85  # inverter, cabling, soiling: ~15% losses

    @property
    def usable_area(self) -> float:
        # Assume 85% of roof area is usable (edge zones, vents, etc.)
        return self.roof_area_m2 * 0.85

    @property
    def max_panels(self) -> int:
        return int(self.usable_area // self.panel_area_m2)

    @property
    def system_size_kwp(self) -> float:
        return (self.max_panels * self.panel_wattage) / 1000

    def _nearest_tilt_factor(self) -> float:
        nearest = min(TILT_FACTORS.keys(), key=lambda t: abs(t - self.tilt_degrees))
        return TILT_FACTORS[nearest]

    @property
    def annual_generation_kwh(self) -> float:
        orient = ORIENTATION_FACTORS.get(self.orientation, 0.85)
        tilt = self._nearest_tilt_factor()
        effective_irr = BASE_IRRADIANCE_KWH_M2 * orient * tilt * self.shading_factor
        # kWh = kWp * effective irradiance * system losses
        return self.system_size_kwp * effective_irr * self.system_losses

    @property
    def estimated_grant_eur(self) -> float:
        grant = 0
        remaining = self.system_size_kwp
        for low, high, rate in SEAI_GRANT_STRUCTURE:
            band = max(0, min(remaining, high - low))
            grant += band * rate
            remaining -= band
        return min(grant, SEAI_GRANT_CAP)


def report(pv: PVSystem):
    print('\n=== SOLAR PV SYSTEM DESIGN ===')
    print(f'Roof area: {pv.roof_area_m2} m2')
    print(f'Orientation: {pv.orientation}, tilt: {pv.tilt_degrees} deg')
    print(f'Shading factor: {pv.shading_factor}')
    print(f'\nUsable roof area: {pv.usable_area:.1f} m2')
    print(f'Max panels ({pv.panel_wattage}W each): {pv.max_panels}')
    print(f'System size: {pv.system_size_kwp:.2f} kWp')
    print(f'Estimated annual generation: {pv.annual_generation_kwh:.0f} kWh/yr')
    print(f'Estimated SEAI grant: EUR {pv.estimated_grant_eur:.0f}')
    # Rough self-consumption: 30-40% without battery, 60-70% with
    self_consumption_no_batt = pv.annual_generation_kwh * 0.35
    grid_export = pv.annual_generation_kwh - self_consumption_no_batt
    print(f'\nEstimated self-consumption (no battery): {self_consumption_no_batt:.0f} kWh/yr')
    print(f'Estimated grid export: {grid_export:.0f} kWh/yr')


if __name__ == '__main__':
    # Example: typical Cork semi, south-west roof, 35 m2, 30 deg tilt
    system = PVSystem(
        roof_area_m2=35,
        orientation='south_west',
        tilt_degrees=30,
        shading_factor=0.95,
    )
    report(system)