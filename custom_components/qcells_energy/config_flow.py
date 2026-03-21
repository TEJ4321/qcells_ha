import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.core import callback
from .const import DOMAIN, CONF_IP, CONF_PASSWORD, CONF_UPDATE_INTERVAL, CONF_INTEGRATION_MODE, CONF_DISPLAY_PRECISION

@config_entries.HANDLERS.register(DOMAIN)
class QcellsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return QcellsOptionsFlowHandler()

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
                vol.Required(CONF_INTEGRATION_MODE, default="simple"): vol.In(["simple", "detailed"]),
                vol.Required(CONF_UPDATE_INTERVAL, default=10): float,
                vol.Required(CONF_DISPLAY_PRECISION, default=2): int,
            }),
            errors=errors,
        )

class QcellsOptionsFlowHandler(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Grab the current settings from options, falling back to data (initial setup)
        current_mode = self.config_entry.options.get(
            CONF_INTEGRATION_MODE, self.config_entry.data.get(CONF_INTEGRATION_MODE, "simple")
        )
        current_interval = self.config_entry.options.get(
            CONF_UPDATE_INTERVAL, self.config_entry.data.get(CONF_UPDATE_INTERVAL, 10)
        )
        current_precision = self.config_entry.options.get(
            CONF_DISPLAY_PRECISION, self.config_entry.data.get(CONF_DISPLAY_PRECISION, 2)
        )

        options_schema = vol.Schema({
            vol.Required(CONF_INTEGRATION_MODE, default=current_mode): vol.In(["simple", "detailed"]),
            vol.Required(CONF_UPDATE_INTERVAL, default=current_interval): float,
            vol.Required(CONF_DISPLAY_PRECISION, default=current_precision): int,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )
