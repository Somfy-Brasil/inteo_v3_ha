from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.exceptions import ConfigEntryAuthFailed
from .const import DOMAIN
import jwt
import time
import datetime



_LOGGER = logging.getLogger(__name__)

# Plataformas suportadas
PLATFORMS = ["cover"]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Inteo component."""
    _LOGGER.info("Inteo component setup started")
    
    # Register OAuth2 implementation with PKCE
    implementation = config_entry_oauth2_flow.LocalOAuth2ImplementationWithPkce(
        hass,
        DOMAIN,
        "inteov3-HA",
        "https://inteoapp.cloudsync.services/assistants/ha/authorize",
        "https://inteoapp.cloudsync.services/api/oauth/token",
        client_secret="",  # PKCE doesn't use client_secret
        code_verifier_length=128
    )
    
    config_entry_oauth2_flow.async_register_implementation(
        hass,
        DOMAIN,
        implementation,
    )
    
    _LOGGER.info("OAuth2 implementation registered")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Inteo from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Check if we have refresh token
    token_data = entry.data.get("token", {})
    if "refresh_token" not in token_data:
        _LOGGER.error("⚠️  REFRESH TOKEN NOT FOUND - reconfiguration will be needed")
    else:
        _LOGGER.debug("✅ Refresh token available for automatic renewal")
    
    # Store entry and implementation for use by devices
    hass.data[DOMAIN]["entry"] = entry
    hass.data[DOMAIN]["implementation"] = None
    
    # Try to get the registered OAuth2 implementation
    try:
        implementations = await config_entry_oauth2_flow.async_get_implementations(hass, DOMAIN)
        if implementations:
            hass.data[DOMAIN]["implementation"] = list(implementations.values())[0]
            _LOGGER.debug("OAuth2 implementation obtained successfully")
        else:
            _LOGGER.debug("No OAuth2 implementation found")
    except Exception as e:
        _LOGGER.warning("Could not get OAuth2 implementation: %s", e)

    _LOGGER.info("Querying Inteo devices...")

    # Get current token
    token_data = entry.data.get("token", {})
    access_token = token_data.get("access_token")
    
    if not access_token:
        _LOGGER.error("Access token not found in configuration")
        return False

    # Check if token is expired before making the request
    if _is_token_expired(access_token):
        _LOGGER.info("Token expired detected, trying to renew before querying devices...")
        if await _try_refresh_token(hass, entry):
            # Get new token after renewal
            updated_token_data = entry.data.get("token", {})
            access_token = updated_token_data.get("access_token")
            _LOGGER.info("Token renewed successfully for device query")
        else:
            _LOGGER.error("Failed to renew token for device query")
            return False

    try:
        session = async_get_clientsession(hass)
        async with session.post(
            "https://inteoapp.cloudsync.services/api/oauth/resources",
            json={"access_token": access_token, "service": "homeassistant"},
            timeout=10,
        ) as resp:
            if resp.status == 401:
                _LOGGER.error("Invalid or expired access token")
                # Try to refresh token if available
                if await _try_refresh_token(hass, entry):
                    _LOGGER.info("Token renewed successfully, trying again...")
                    return await async_setup_entry(hass, entry)  # Try again
                else:
                    raise ConfigEntryAuthFailed("Token expired, reauthentication needed")
            
            if resp.status != 200:
                _LOGGER.error("Error fetching Inteo resources: %s", resp.status)
                return False

            data = await resp.json()
            endpoints = data.get("endpoints", [])
            _LOGGER.info("Inteo devices found: %s", endpoints)

            hass.data[DOMAIN]["endpoints"] = endpoints

            await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    except ConfigEntryAuthFailed:
        _LOGGER.error("Token expired, starting reauthentication process...")
        raise
    except Exception as e:
        _LOGGER.exception("Error querying Inteo devices: %s", e)
        return False

    return True


async def _try_refresh_token(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Try to refresh OAuth2 token."""
    try:
        token_data = entry.data.get("token", {})
        refresh_token = token_data.get("refresh_token")
        
        _LOGGER.debug("Starting token renewal...")
        _LOGGER.debug("Token data keys: %s", list(token_data.keys()))
        
        if not refresh_token:
            _LOGGER.error("Refresh token not available in data: %s", token_data)
            return False
        
        _LOGGER.debug("Refresh token available: %s...", refresh_token[:20])
        
        session = async_get_clientsession(hass)
        
        # Data for token renewal (PKCE)
        refresh_data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": "inteov3-HA",
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        _LOGGER.debug("Sending refresh request to: https://inteoapp.cloudsync.services/api/oauth/token")
        
        # Make request to renew token (without client_secret)
        async with session.post(
            "https://inteoapp.cloudsync.services/api/oauth/token",
            data=refresh_data,
            headers=headers,
            timeout=10,
        ) as resp:
            response_text = await resp.text()
            _LOGGER.debug("Response status: %s", resp.status)
            _LOGGER.debug("Response body: %s", response_text)
            
            if resp.status != 200:
                _LOGGER.error("Failed to renew token: HTTP %s - %s", resp.status, response_text)
                return False
            
            new_token_data = await resp.json()
            _LOGGER.debug("New token received: %s", list(new_token_data.keys()))
            
            # Update entry with new token
            new_data = dict(entry.data)
            new_data["token"]["access_token"] = new_token_data.get("access_token")
            if "refresh_token" in new_token_data:
                new_data["token"]["refresh_token"] = new_token_data.get("refresh_token")
            
            hass.config_entries.async_update_entry(entry, data=new_data)
            _LOGGER.info("Token renewed successfully - new access_token: %s...", 
                        new_token_data.get("access_token", "")[:20])
            return True
            
    except Exception as e:
        _LOGGER.exception("Error renewing token: %s", e)
        return False


def _is_token_expired(token: str) -> bool:
    """Check if JWT token is expired locally."""
    try:
        # Decode JWT without verifying signature (just to read claims)
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        # Check if it has 'exp' field (expiration)
        if 'exp' not in decoded:
            _LOGGER.debug("Token doesn't have 'exp' field, assuming valid")
            return False
        
        # Check if expired (with 30 second margin)
        current_time = int(time.time())
        expiration_time = decoded['exp']
        margin = 30  # 30 seconds
        
        # Debug: Show complete JWT information
        _LOGGER.debug("JWT Debug - iat: %s, exp: %s, expected duration: %d seconds", 
                     decoded.get('iat', 'N/A'), decoded.get('exp', 'N/A'), 
                     expiration_time - decoded.get('iat', current_time))
        
        # Debug: Show timestamps in readable format
        exp_datetime = datetime.datetime.fromtimestamp(expiration_time, tz=datetime.timezone.utc)
        current_datetime = datetime.datetime.fromtimestamp(current_time, tz=datetime.timezone.utc)
        
        is_expired = current_time >= (expiration_time - margin)
        time_until_expiry = expiration_time - current_time
        
        if is_expired:
            _LOGGER.debug("Token expired - exp: %s (%s), current: %s (%s)", 
                         expiration_time, exp_datetime.strftime("%H:%M:%S UTC"), 
                         current_time, current_datetime.strftime("%H:%M:%S UTC"))
        else:
            _LOGGER.debug("Token valid - exp: %s (%s), current: %s (%s), remaining: %d seconds", 
                         expiration_time, exp_datetime.strftime("%H:%M:%S UTC"),
                         current_time, current_datetime.strftime("%H:%M:%S UTC"), 
                         time_until_expiry)
            
        return is_expired
        
    except Exception as e:
        _LOGGER.warning("Error checking token expiration: %s", e)
        return False  # In case of error, assume valid


async def async_get_valid_token(hass: HomeAssistant) -> str | None:
    """Get a valid token, renewing if necessary."""
    entry = hass.data[DOMAIN].get("entry")
    if not entry:
        _LOGGER.error("Entry not found to get token")
        return None
    
    token_data = entry.data.get("token", {})
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    
    if not access_token:
        _LOGGER.error("Access token not found in entry data")
        return None
    
    # Check if current token is expired
    if _is_token_expired(access_token):
        _LOGGER.info("Token expired detected locally, trying to renew...")
        
        if refresh_token:
            if await _try_refresh_token(hass, entry):
                # Get new token after renewal
                updated_token_data = entry.data.get("token", {})
                new_access_token = updated_token_data.get("access_token")
                _LOGGER.info("Token renewed successfully: %s...", new_access_token[:20] if new_access_token else "None")
                return new_access_token
            else:
                _LOGGER.error("Failed to renew expired token")
                return None
        else:
            _LOGGER.error("Token expired and no refresh_token available")
            return None
    else:
        _LOGGER.debug("Current token is valid: %s...", access_token[:20])
        return access_token


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)