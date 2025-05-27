import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from .const import DOMAIN, CONF_IP, CONF_PASSWORD, CONF_UPDATE_INTERVAL

@config_entries.HANDLERS.register(DOMAIN)
class QcellsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=f"Qcells at {user_input[CONF_IP]}", data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_IP, default="myqhome"): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_UPDATE_INTERVAL, default=10): int,
            }),
            errors=errors,
        )
