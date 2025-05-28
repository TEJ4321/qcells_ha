from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

SENSOR_TYPES = {
    "battery_power": ["Battery Power", "W", lambda d: d["ess_all"]["inverter_info"]["bdc"]["power"]],
    "grid_power": ["Grid Active Power", "W", lambda d: d["meter_info"]["grid_active_power"]],
    "pv1": ["PV Power 1", "W", lambda d: d["ess_all"]["pv_info"]["power"][0]],
    "pv2": ["PV Power 2", "W", lambda d: d["ess_all"]["pv_info"]["power"][1]],
    "soc": ["State of Charge", "%", lambda d: d["current_avg_soc"]],
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [QcellsSensor(coordinator, entry, key, *val) for key, val in SENSOR_TYPES.items()]
    async_add_entities(sensors)

class QcellsSensor(SensorEntity):
    def __init__(self, coordinator, entry, key, name, unit, value_fn):
        self._attr_name = f"Qcells {name}"
        self._attr_unit_of_measurement = unit
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
            "configuration_url": f"http://{self._entry.data.get('ip_address')}:7000/",
        }