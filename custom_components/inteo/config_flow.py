from __future__ import annotations

import logging

from homeassistant import config_entries, data_entry_flow
from homeassistant.helpers import config_entry_oauth2_flow
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Flag para evitar registros duplicados
_config_flow_oauth2_registered = False

async def _ensure_oauth2_implementation(hass):
    """Ensure OAuth2 implementation is registered."""
    global _config_flow_oauth2_registered
    
    if _config_flow_oauth2_registered:
        return
        
    _LOGGER.info("Config Flow: Registering OAuth2 PKCE implementation...")
    
    # Register PKCE implementation
    implementation = config_entry_oauth2_flow.LocalOAuth2ImplementationWithPkce(
        hass,
        DOMAIN,
        "inteov3-HA",
        "https://inteoapp.cloudsync.services/assistants/ha/authorize",
        "https://inteoapp.cloudsync.services/api/oauth/token",
        client_secret="",  # PKCE doesn't use client_secret
        code_verifier_length=128
    )
    _LOGGER.info("✅ PKCE implementation created successfully")
    
    config_entry_oauth2_flow.async_register_implementation(
        hass,
        DOMAIN,
        implementation,
    )
    
    _config_flow_oauth2_registered = True
    _LOGGER.info("Config Flow: OAuth2 PKCE implementation registered!")

class InteoOAuth2FlowHandler(config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN):
    """Handle a config flow for Inteo using OAuth2."""

    DOMAIN = DOMAIN
    VERSION = 1

    @property
    def logger(self) -> logging.Logger:
        return _LOGGER

    @property
    def extra_authorize_data(self) -> dict:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "scope": "read",
        }

    async def async_oauth_create_entry(self, data: dict) -> data_entry_flow.FlowResult:
        """Create an entry for the flow."""
        # Check if refresh token was received
        if "token" in data:
            token_data = data["token"]
            if "refresh_token" in token_data:
                _LOGGER.info("✅ OAuth2 PKCE configured successfully")
            else:
                _LOGGER.error("❌ Refresh token not received from OAuth2 server")
        else:
            _LOGGER.error("❌ No token found in OAuth2 response")
        
        # Check if we have the required data
        if "token" not in data:
            _LOGGER.error("Token not found in OAuth2 data")
            return self.async_abort(reason="missing_token")
        
        return self.async_create_entry(title="Inteo", data=data)

    async def async_step_user(self, user_input=None):
        """Handle a flow start initiated by the user."""
        # Ensure OAuth2 is registered
        await _ensure_oauth2_implementation(self.hass)
        
        return await super().async_step_user(user_input)

    async def async_step_reauth(self, entry_data):
        """Handle a reauthentication flow."""
        self._entry_data = entry_data
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        """Confirm reauthentication."""
        if user_input is not None:
            return await self.async_step_user()
        return self.async_show_form(step_id="reauth_confirm")