# coordinator.py
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN
import logging
import async_timeout
from aiohttp import FormData

_LOGGER = logging.getLogger(__name__)

class QcellsDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, ip: str, password: str, update_interval: timedelta):
        super().__init__(
            hass,
            _LOGGER,
            name="Qcells Energy Coordinator",
            update_interval=update_interval,
        )
        self._ip = ip
        self._password = password
        self._session = async_get_clientsession(hass, verify_ssl=False)

    async def _async_login(self):
        login_url = f"https://{self._ip}:7000/login"

        form = FormData()
        form.add_field("pswd", self._password)  # Postman does NOT send "name=Login"
        
        async with self._session.post(login_url, data=form) as resp:
            if resp.status != 200:
                raise UpdateFailed(f"Login failed: {resp.status}")
            _LOGGER.debug("Login successful")

    async def _async_update_data(self):
        try:
            await self._async_login()

            status_url = f"https://{self._ip}:7000/system/status/pcssystem"
            async with async_timeout.timeout(10):
                async with self._session.get(status_url, headers={"Accept": "application/json"}) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"Error fetching Qcells data: {resp.status}")
                    data = await resp.json(content_type=None)
                    return data

        except Exception as err:
            raise UpdateFailed(f"Error fetching Qcells data: {err}")
