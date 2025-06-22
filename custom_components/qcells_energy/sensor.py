from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util
from functools import cached_property

SENSOR_TYPES = {
    # Battery
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
    "battery_voltage": [
        "Battery Voltage", "V", "voltage",
        lambda d: d["ess_all"]["inverter_info"]["bdc"]["voltage"]
    ],
    "battery_current": [
        "Battery Current", "A", "current",
        lambda d: d["ess_all"]["inverter_info"]["bdc"]["current"][0]
    ],
    "battery_rack_voltage": [
        "Battery Rack Voltage", "V", "voltage",
        lambda d: d["ess_all"]["bat_info"]["bat_rack_info"][0]["rack_voltage"]
    ],
    "battery_rack_current": [
        "Battery Rack Current", "A", "current",
        lambda d: d["ess_all"]["bat_info"]["bat_rack_info"][0]["rack_current"]
    ],
    "battery_avg_cell_temp": [
        "Battery Avg Cell Temperature", "°C", "temperature",
        lambda d: d["ess_all"]["bat_info"]["bat_rack_info"][0]["avg_cell_temperature"]
    ],
    "battery_max_cell_temp": [
        "Battery Max Cell Temperature", "°C", "temperature",
        lambda d: d["ess_all"]["bat_info"]["bat_rack_info"][0]["max_cell_temperature"]
    ],
    "battery_min_cell_temp": [
        "Battery Min Cell Temperature", "°C", "temperature",
        lambda d: d["ess_all"]["bat_info"]["bat_rack_info"][0]["min_cell_temperature"]
    ],
    "battery_soh": [
        "Battery State of Health", "%", "battery",
        lambda d: d["ess_all"]["bat_info"]["bat_rack_info"][0]["soh"]
    ],
    "battery_charge_cycle_count": [
        "Battery Charge Cycle Count", "", "none",
        lambda d: d["ess_all"]["bat_info"]["bat_history_info"][0]["charge_cycle_count"]
    ],
    "battery_discharge_cycle_count": [
        "Battery Discharge Cycle Count", "", "none",
        lambda d: d["ess_all"]["bat_info"]["bat_history_info"][0]["discharge_cycle_count"]
    ],
    "battery_total_charge": [
        "Battery Total Charge", "kWh", "energy",
        lambda d: d["ess_all"]["bat_info"]["bat_history_info"][0]["total_charge_amount_wh"]/1000
    ],
    "battery_total_discharge": [
        "Battery Total Discharge", "kWh", "energy",
        lambda d: d["ess_all"]["bat_info"]["bat_history_info"][0]["total_discharge_amount_wh"]/1000
    ],
    "soc": [
        "Battery State of Charge", "%", "battery",
        lambda d: d["current_avg_soc"]
    ],
    "battery_charging_state": [
        "Battery Charging State", "", "enum",
        lambda d: (
            "Charging" if d["ess_all"]["inverter_info"]["bdc"]["power"] < -0.5
            else "Discharging" if d["ess_all"]["inverter_info"]["bdc"]["power"] > 0.5
            else "Standby"
        )
    ],

    # PV
    "pv1": [
        "Solar Array 1 Power", "W", "power",
        lambda d: d["ess_all"]["pv_info"]["power"][0]
    ],
    "pv2": [
        "Solar Array 2 Power", "W", "power",
        lambda d: d["ess_all"]["pv_info"]["power"][1]
    ],
    "pv_total_power": [
        "Total Solar Power", "W", "power",
        lambda d: d["ess_all"]["pv_info"]["total_power"]
    ],
    "pv1_voltage": [
        "Solar Array 1 Voltage", "V", "voltage",
        lambda d: d["ess_all"]["pv_info"]["voltage"][0]
    ],
    "pv2_voltage": [
        "Solar Array 2 Voltage", "V", "voltage",
        lambda d: d["ess_all"]["pv_info"]["voltage"][1]
    ],
    "pv1_current": [
        "Solar Array 1 Current", "A", "current",
        lambda d: d["ess_all"]["pv_info"]["current"][0]
    ],
    "pv2_current": [
        "Solar Array 2 Current", "A", "current",
        lambda d: d["ess_all"]["pv_info"]["current"][1]
    ],

    # Grid
    "grid_power": [
        "Grid Active Power", "W", "power",
        lambda d: d["meter_info"]["grid_active_power"]
    ],
    "grid_power_consumption": [ 
        "Grid Power Consumption", "W", "power",
        lambda d: max(d["meter_info"]["grid_active_power"], 0)
    ],
    "grid_power_return": [
        "Grid Power Return", "W", "power",
        lambda d: abs(min(d["meter_info"]["grid_active_power"], 0))
    ],
    "grid_voltage": [
        "Grid Voltage", "V", "voltage",
        lambda d: d["meter_info"]["grid_voltage"]
    ],
    "grid_current": [
        "Grid Current", "A", "current",
        lambda d: d["meter_info"]["grid_current"]
    ],
    "grid_power_factor": [
        "Grid Power Factor", "", "power_factor",
        lambda d: d["meter_info"]["grid_power_factor"]
    ],
    "grid_frequency": [
        "Grid Frequency", "Hz", "frequency",
        lambda d: d["meter_info"]["grid_hz"]
    ],
    "grid_reactive_power": [
        "Grid Reactive Power", "var", "reactive_power",
        lambda d: d["meter_info"]["grid_reactive_power"]
    ],

    # Inverter
    "inverter_active_power": [
        "Inverter Active Power", "W", "power",
        lambda d: d["ess_all"]["inverter_info"]["inv"]["active_power"]
    ],
    "inverter_apparent_power": [
        "Inverter Apparent Power", "VA", "apparent_power",
        lambda d: d["ess_all"]["inverter_info"]["inv"]["apparent_power"]
    ],
    "inverter_voltage": [
        "Inverter Voltage", "V", "voltage",
        lambda d: d["ess_all"]["inverter_info"]["inv"]["voltage"]
    ],
    "inverter_current": [
        "Inverter Current", "A", "current",
        lambda d: d["ess_all"]["inverter_info"]["inv"]["current"]
    ],
    "inverter_frequency": [
        "Inverter Frequency", "Hz", "frequency",
        lambda d: d["ess_all"]["inverter_info"]["inv"]["frequency"]
    ],
    "inverter_power_factor": [
        "Inverter Power Factor", "", "power_factor",
        lambda d: d["ess_all"]["inverter_info"]["inv"]["power_factor"]
    ],
    "inverter_temperature": [
        "Inverter Temperature", "°C", "temperature",
        lambda d: d["ess_all"]["inverter_info"]["temperature"]["inverter"]
    ],

    # System/Status
    "system_temperature": [
        "System Temperature", "°C", "temperature",
        lambda d: d["ess_all"]["inverter_info"]["temperature"]["system"]
    ],
    "battery_status_flag": [
        "Battery Status Flag", "", "none",
        lambda d: d["ess_all"]["bat_info"]["bat_rack_info"][0]["battery_status_flag"]
    ],
    "simulation_mode_enabled": [
        "Simulation Mode Enabled", "", "none",
        lambda d: d["simulation_mode"]["simulation_enable_flag"]
    ],
    "auto_charge_discharge_enabled": [
        "Auto Charge/Discharge Enabled", "", "none",
        lambda d: d["simulation_mode"]["auto_charge_discharge_enable_flag"]
    ],

    # Error/Alarm
    "current_fault_history_size": [
        "Current Fault History Size", "", "none",
        lambda d: d["error_history"]["currentFaultHistorySize"]
    ],
    "current_fault_list": [
        "Current Fault List", "", "none",
        lambda d: ", ".join(d["error_history"]["currentFaultHistory"]["ems_fault_list"])
    ],

    # Load
    "current_load": [ # This is a virtual sensor that calculates current house load
        "Current Load", "W", "power",
        lambda d: (
            d["ess_all"]["pv_info"]["total_power"] # Total solar power generation (positive)
            - d["meter_info"]["grid_active_power"] # Grid power consumption (negative when exporting)
            + d["ess_all"]["inverter_info"]["bdc"]["power"] # Battery power use (negative when charging)
        )
    ],
}

ICON_MAP = {
    # Battery
    "battery_power": "mdi:battery-charging",
    "battery_power_energy": "mdi:battery-charging-outline",
    "battery_power_charging": "mdi:battery-arrow-up",
    "battery_power_charging_energy": "mdi:battery-arrow-up-outline",
    "battery_power_discharging": "mdi:battery-arrow-down",
    "battery_power_discharging_energy": "mdi:battery-arrow-down-outline",
    "battery_voltage": "mdi:car-battery",
    "battery_current": "mdi:current-dc",
    "battery_rack_voltage": "mdi:car-battery",
    "battery_rack_current": "mdi:current-dc",
    "battery_avg_cell_temp": "mdi:thermometer",
    "battery_max_cell_temp": "mdi:thermometer-high",
    "battery_min_cell_temp": "mdi:thermometer-low",
    "battery_soh": "mdi:battery-heart",
    "battery_charge_cycle_count": "mdi:counter",
    "battery_discharge_cycle_count": "mdi:counter",
    "battery_total_charge": "mdi:battery-plus",
    "battery_total_discharge": "mdi:battery-minus",
    # PV
    "pv1": "mdi:solar-power",
    "pv1_energy": "mdi:solar-power-variant",
    "pv2": "mdi:solar-power",
    "pv2_energy": "mdi:solar-power-variant",
    "pv_total_power": "mdi:solar-power",
    "pv_total_energy": "mdi:solar-power-variant",
    "pv1_voltage": "mdi:flash",
    "pv2_voltage": "mdi:flash",
    "pv1_current": "mdi:current-dc",
    "pv2_current": "mdi:current-dc",
    # Grid
    "grid_power": "mdi:transmission-tower",
    "grid_power_energy": "mdi:transmission-tower",
    "grid_power_consumption": "mdi:transmission-tower-export",
    "grid_power_consumption_energy": "mdi:transmission-tower-export",
    "grid_power_return": "mdi:transmission-tower-import",
    "grid_power_return_energy": "mdi:transmission-tower-import",
    "grid_voltage": "mdi:flash",
    "grid_current": "mdi:current-ac",
    "grid_power_factor": "mdi:sigma",
    "grid_frequency": "mdi:sine-wave",
    "grid_reactive_power": "mdi:flash-outline",
    # Inverter
    "inverter_active_power": "mdi:lightning-bolt",
    "inverter_active_energy": "mdi:lightning-bolt-outline",
    "inverter_apparent_power": "mdi:lightning-bolt-outline",
    "inverter_apparent_energy": "mdi:lightning-bolt-circle",
    "inverter_voltage": "mdi:flash",
    "inverter_current": "mdi:current-ac",
    "inverter_frequency": "mdi:sine-wave",
    "inverter_power_factor": "mdi:sigma",
    "inverter_temperature": "mdi:thermometer",
    # System/Status
    "system_temperature": "mdi:thermometer",
    "battery_status_flag": "mdi:alert",
    "simulation_mode_enabled": "mdi:toggle-switch",
    "auto_charge_discharge_enabled": "mdi:toggle-switch",
    # Error/Alarm
    "current_fault_history_size": "mdi:alert-circle",
    "current_fault_list": "mdi:alert-box",
    # Load
    "current_load": "mdi:home-lightning-bolt",
    "current_load_energy": "mdi:home-lightning-bolt-outline",
}

SENSOR_DEVICE_MAP = {
    # Battery
    "battery_power": "battery",
    "battery_power_charging": "battery",
    "battery_power_discharging": "battery",
    "battery_voltage": "battery",
    "battery_current": "battery",
    "battery_rack_voltage": "battery",
    "battery_rack_current": "battery",
    "battery_avg_cell_temp": "battery",
    "battery_max_cell_temp": "battery",
    "battery_min_cell_temp": "battery",
    "battery_soh": "battery",
    "battery_charge_cycle_count": "battery",
    "battery_discharge_cycle_count": "battery",
    "battery_total_charge": "battery",
    "battery_total_discharge": "battery",
    "battery_charging_state": "battery",
    "soc": "battery",

    # PV
    "pv1": "pv",
    "pv2": "pv",
    "pv_total_power": "pv",
    "pv1_voltage": "pv",
    "pv2_voltage": "pv",
    "pv1_current": "pv",
    "pv2_current": "pv",

    # Grid
    "grid_power": "grid",
    "grid_power_consumption": "grid",
    "grid_power_return": "grid",
    "grid_voltage": "grid",
    "grid_current": "grid",
    "grid_power_factor": "grid",
    "grid_frequency": "grid",
    "grid_reactive_power": "grid",

    # Inverter
    "inverter_active_power": "inverter",
    "inverter_apparent_power": "inverter",
    "inverter_voltage": "inverter",
    "inverter_current": "inverter",
    "inverter_frequency": "inverter",
    "inverter_power_factor": "inverter",
    "inverter_temperature": "inverter",

    # System/Status/Error/Load
    "system_temperature": "system",
    "battery_status_flag": "system",
    "simulation_mode_enabled": "system",
    "auto_charge_discharge_enabled": "system",
    "current_fault_history_size": "system",
    "current_fault_list": "system",
    "current_load": "system",
}

DEVICE_INFO_MAP = {
    "battery": {
        "name": "Qcells Battery",
        "model": "Q.SAVE Battery",
    },
    "pv": {
        "name": "Qcells Solar Array",
        "model": "Q.Home PV",
    },
    "grid": {
        "name": "Electricity Grid",
        "model": "N/A",
    },
    "inverter": {
        "name": "Qcells Inverter",
        "model": "Q.VOLT Inverter",
    },
    "system": {
        "name": "Qcells System",
        "model": "Q.Home System",
    },
}

SIMPLE_SENSOR_KEYS = [
    "soc",
    "battery_power",
    "battery_power_charging",
    "battery_power_discharging",
    "battery_voltage",
    "battery_current",
    "battery_soh",
    "battery_charging_state",
    "battery_avg_cell_temp",
    "pv_total_power",
    "current_load",
    "system_temperature",
    "grid_power",
    "grid_power_consumption",
    "grid_power_return",
    "grid_voltage",
    "grid_current",
    "grid_frequency",
    "inverter_active_power",
    "inverter_voltage",
    "inverter_current",
    "inverter_frequency",
]

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    integration_mode = entry.data.get("integration_mode", "simple")
    display_precision = entry.data.get("display_precision", 2)

    if integration_mode == "simple":
        sensor_keys = SIMPLE_SENSOR_KEYS
    else:
        sensor_keys = list(SENSOR_TYPES.keys())

    # Main sensors
    # =======================================================================================
    sensors = [
        QcellsSensor(coordinator, entry, key, name, unit, sensor_type, value_fn, display_precision)
        for key in sensor_keys
        for (name, unit, sensor_type, value_fn) in [SENSOR_TYPES[key]]
    ]
    async_add_entities(sensors)

    # Virtual energy sensors
    # =======================================================================================
    virtual_sensors = []
    # Add virtual energy sensors for all power sensors (that are exposed based on simple/detailed mode)
    for key, val in SENSOR_TYPES.items():
        name, unit, sensor_type, _ = val
        if unit == "W":  # Only for power sensors
            group = SENSOR_DEVICE_MAP.get(key, "system")
            # Replace "Power" with "Energy" only if present, otherwise just use the name
            if "Power" in name:
                energy_name = name.replace("Power", "Energy").strip()
            else:
                energy_name = f"{name} Energy"
            virtual_sensors.append(
                QcellsVirtualEnergySensor(coordinator, entry, key, energy_name, group, display_precision)
            )
    async_add_entities(virtual_sensors)


class QcellsSensor(SensorEntity):
    def __init__(self, coordinator, entry, key, name, unit, sensor_type, value_fn, display_precision):
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = sensor_type
        self.coordinator = coordinator
        self.value_fn = value_fn
        self._attr_unique_id = f"qcells_{key}"
        self._entry = entry
        self._sensor_key = key
        self._attr_suggested_display_precision = display_precision
        self._attr_icon = ICON_MAP.get(key, None)
        group = SENSOR_DEVICE_MAP.get(self._sensor_key, "system")
        info = DEVICE_INFO_MAP[group]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{self._entry.entry_id}_{group}")},
            "name": info["name"],
            "manufacturer": "Qcells",
            "model": info["model"],
            "configuration_url": f"https://{self._entry.data.get('ip_address')}:7000/",
        }

    @cached_property
    def icon(self) -> str | None:
        # Dynamic icon for battery_charging_state
        if self._sensor_key == "battery_charging_state":
            state = getattr(self, "native_value", None)
            if state == "Charging":
                return "mdi:battery-arrow-up_outline"
            elif state == "Discharging":
                return "mdi:battery-arrow-down_outline"
            elif state == "Standby":
                return "mdi:battery_check_outline"
            else:
                return "mdi:battery"
        return self._attr_icon

    async def async_update(self):
        await self.coordinator.async_request_refresh()
        try:
            value = self.value_fn(self.coordinator.data)
            self._attr_native_value = value
        except Exception:
            self._attr_native_value = None
        self._attr_available = self.coordinator.last_update_success

class QcellsVirtualEnergySensor(RestoreEntity, SensorEntity):
    """Virtual energy sensor that integrates power over time."""

    def __init__(self, coordinator, entry, power_sensor_key, name, device_group, display_precision):
        self.coordinator = coordinator
        self._entry = entry
        # Remove "Power" from the name if present, and remove trailing whitespace
        if "Power" in name:
            name = name.replace("Power", "Energy").strip()
        self._power_sensor_key = power_sensor_key
        self._attr_name = name
        self._attr_unique_id = f"qcells_{power_sensor_key}_virtual_energy"
        self._attr_native_unit_of_measurement = "kWh"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._last_update = None
        self._energy = 0.0
        self._device_group = device_group
        self._attr_suggested_display_precision = display_precision

        # Use a different icon for energy sensors
        energy_icon_key = f"{power_sensor_key}_energy"
        self._attr_icon = ICON_MAP.get(energy_icon_key, "mdi:lightning-bolt-outline")


        # Use the value function from SENSOR_TYPES
        self._value_fn = SENSOR_TYPES[power_sensor_key][3]

        group = self._device_group
        info = DEVICE_INFO_MAP[group]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{self._entry.entry_id}_{group}")},
            "name": info["name"],
            "manufacturer": "Qcells",
            "model": info["model"],
            "configuration_url": f"https://{self._entry.data.get('ip_address')}:7000/",
        }

    async def async_added_to_hass(self):
        last_state = await self.async_get_last_state()
        if last_state is not None and last_state.state not in (None, "unknown", "unavailable"):
            try:
                self._energy = float(last_state.state)
            except ValueError:
                self._energy = 0.0
        self._last_update = dt_util.utcnow()

    async def async_update(self):
        # Called by HA to update the sensor
        await self.async_calculate_energy()
        self._attr_native_value = self._energy

    async def async_calculate_energy(self):
        """Calculate energy based on power sensor data."""
        if not self.coordinator.data or not self.coordinator.last_update_success:
            return

        current_time = dt_util.utcnow()
        try:
            power_value = self._value_fn(self.coordinator.data)
        except Exception:
            power_value = None

        # power_value = self.coordinator.data.get(self._power_sensor_key)

        if power_value is None or self._last_update is None:
            self._last_update = current_time
            return

        # Calculate time difference in seconds
        time_diff = (current_time - self._last_update).total_seconds()
        if time_diff <= 0:
            self._last_update = current_time
            return

        # Convert power to kW and calculate energy in kWh
        energy_delta = (power_value / 1000) * (time_diff / 3600)  # kWh
        self._energy += energy_delta
        self._last_update = current_time
