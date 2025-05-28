# coordinator.py
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
# from homeassistant.helpers.aiohttp_client import async_get_clientsession
import requests
# from .const import DOMAIN
import logging
import async_timeout

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

    def _login(self):
        login_url = f"https://{self._ip}:7000/login"
        data = f"pswd={self._password}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        print(f"Sending login POST to {login_url} with:\nHeaders: {headers}\nData: {data}\n======================================================")
        
        session = requests.Session()

        try:
            resp = session.post(login_url, data=data, headers=headers, verify=False, timeout=10)
            # print(f"Login response status: {resp.status_code}\nHeaders: {resp.headers}\nBody: {resp.text}")
            if resp.status_code != 200:
                raise UpdateFailed(f"Login failed: {resp.status_code}, body: {resp.text[:300]}")
            # Check for session cookie
            session_cookie = None
            for cookie in session.cookies:
                # print(f"Cookie received: {cookie.name}={cookie.value}")
                if "installer_session" in cookie.name:
                    session_cookie = cookie
            if not session_cookie:
                raise UpdateFailed("Login failed: No session cookie received")
            
            # print("Login successful")
            return session
        
        except Exception as err:
            raise UpdateFailed(f"Error during login: {err}")

    def _get_status(self, session):
        status_url = f"https://{self._ip}:7000/system/status/pcssystem"
        try:
            resp = session.get(status_url, headers={"Accept": "application/json"}, verify=False, timeout=10)
            if resp.status_code != 200:
                raise UpdateFailed(f"Error reading Qcells data: {resp.status_code}")
            return resp.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching Qcells data: {err}")
        
    async def _async_update_data(self):
        # Run sync code in executor
        return await self.hass.async_add_executor_job(self._sync_update_data)

    def _sync_update_data(self):
        session = self._login()
        return self._get_status(session)