from __future__ import annotations

from homeassistant.components.cover import (
    CoverEntity,
    CoverEntityFeature,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.exceptions import ConfigEntryAuthFailed
from .const import DOMAIN
import logging
import hashlib
import aiohttp

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    endpoints = hass.data[DOMAIN].get("endpoints", [])
    devices = [e for e in endpoints if e.startswith("device;")]

    entities = []

    for dev in devices:
        _, device_id, name, mac = dev.split(";")
        entities.append(InteoCover(device_id, name, mac, entry))

    async_add_entities(entities)


class InteoCover(CoverEntity):

    @staticmethod
    def generate_unique_id(mac, device_id):
        base = f"{mac}_{device_id}"
        return "inteo_" + hashlib.sha1(base.encode()).hexdigest()[:10]  

    def __init__(self, device_id, name, mac, entry):
        self._device_id = device_id
        self._attr_name = name
        self._mac = mac
        self._entry = entry
        self._is_closed = False
        self._attr_unique_id = InteoCover.generate_unique_id(mac, device_id)

    @property
    def supported_features(self):
        return (
            CoverEntityFeature.OPEN
            | CoverEntityFeature.CLOSE
            | CoverEntityFeature.STOP
        )



    @property
    def unique_id(self):
        return self._attr_unique_id
    
    @property
    def is_closed(self) -> bool | None:
        return None

    async def async_open_cover(self, **kwargs):
        await self._send_command(1)
        self._is_closed = False
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs):
        await self._send_command(0)
        self._is_closed = True
        self.async_write_ha_state()

    async def async_stop_cover(self, **kwargs):
        await self._send_command(2)

    async def _send_command(self, action: int):
        """Send command to device with automatic token refresh."""
        from . import async_get_valid_token
        
        _LOGGER.info("Starting command %d%% for device %s", action, self._device_id)
        
        # Get valid token (with automatic renewal if necessary)
        access_token = await async_get_valid_token(self.hass)
        
        if not access_token:
            _LOGGER.error("Could not get valid token for device %s", self._device_id)
            raise ConfigEntryAuthFailed("Invalid token, reauthentication needed")
        
        try:
            async with aiohttp.ClientSession() as session:
                command_data = {
                    "device": {
                        "customData": {
                            "deviceId": self._device_id,
                            "mac": self._mac,
                        }
                    },
                    "action": action,
                }
                
                async with session.post(
                    "https://fsl522jy3x3qirfyil4yytcrd40ernie.lambda-url.us-east-1.on.aws/command",
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    },
                    json=command_data,
                    timeout=10,
                ) as resp:
                    if resp.status == 401:
                        _LOGGER.error("Invalid token when sending command to %s", self._device_id)
                        raise ConfigEntryAuthFailed("Token expired, reauthentication needed")
                    elif resp.status != 200:
                        response_text = await resp.text()
                        _LOGGER.error("Error sending command to %s: HTTP %d - %s", self._device_id, resp.status, response_text)
                        resp.raise_for_status()
                    
                    _LOGGER.info("Command %d%% sent successfully to %s", action, self._device_id)
                    
        except ConfigEntryAuthFailed:
            _LOGGER.error("Authentication failure for device %s", self._device_id)
            raise
        except Exception as e:
            _LOGGER.error("Error sending command to %s: %s", self._device_id, e)
            raise