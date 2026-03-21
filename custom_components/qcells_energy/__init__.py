import asyncio
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import QcellsDataUpdateCoordinator

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the QCells Energy component."""
    # @TODO: Add setup code.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    ip = entry.data["ip_address"]
    password = entry.data["password"]
    
    # Prefer options over data if the user has reconfigured the integration
    update_interval_sec = entry.options.get("update_interval", entry.data.get("update_interval", 10))
    update_interval = timedelta(seconds=int(update_interval_sec))
    
    coordinator = QcellsDataUpdateCoordinator(hass, ip, password, update_interval)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # hass.async_create_task(
    #     hass.config_entries.async_forward_entry_setup(entry, "sensor")
    # )
    # return True

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    # Listen for configuration options updates to reload the component
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)
