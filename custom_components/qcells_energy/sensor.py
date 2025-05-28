from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

SENSOR_TYPES = {
    "battery_power": [
        "Battery Power", "W", "power",
        lambda d: d["ess_all"]["inverter_info"]["bdc"]["power"]
    ],
    "battery_power_charging": [
        "Battery Power Charging", "W", "power",
        lambda d: abs(min(d["ess_all"]["inverter_info"]["bdc"]["power"], 0))
    ],
    "battery_power_discharging": [
        "Battery Power Discharging", "W", "power",
        lambda d: max(d["ess_all"]["inverter_info"]["bdc"]["power"], 0)
    ],
    "grid_power": [
        "Grid Active Power", "W", "power",
        lambda d: d["meter_info"]["grid_active_power"]
    ],
    "current_load": [
        "Current Load", "W", "power",
        lambda d: (
            d["ess_all"]["inverter_info"]["bdc"]["power"]
            + d["meter_info"]["grid_active_power"]
            + d["ess_all"]["pv_info"]["power"][0]
            + d["ess_all"]["pv_info"]["power"][1]
        )
    ],
    "pv1": [
        "PV Power 1", "W", "power",
        lambda d: d["ess_all"]["pv_info"]["power"][0]
    ],
    "pv2": [
        "PV Power 2", "W", "power",
        lambda d: d["ess_all"]["pv_info"]["power"][1]
    ],
    "soc": [
        "State of Charge", "%", "soc",
        lambda d: d["current_avg_soc"]
    ],
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [QcellsSensor(coordinator, entry, key, *val) for key, val in SENSOR_TYPES.items()]
    async_add_entities(sensors)

class QcellsSensor(SensorEntity):
    def __init__(self, coordinator, entry, key, name, unit, sensor_type, value_fn):
        self._attr_name = f"Qcells {name}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = sensor_type
        self.coordinator = coordinator
        self.value_fn = value_fn
        self._attr_unique_id = f"qcells_{key}"
        self._entry = entry

    @property
    def native_value(self) -> float | None: # type: ignore
        try:
            return self.value_fn(self.coordinator.data)
        except Exception:
            return None

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool: # type: ignore[override]
        return self.coordinator.last_update_success
    
    @property
    def device_info(self): # type: ignore
        """Return device information for the Qcells inverter."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Qcells Inverter",
            "manufacturer": "Qcells",
            "model": "Q.Home",
            "configuration_url": f"https://{self._entry.data.get('ip_address')}:7000/",
        }