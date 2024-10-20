from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, Platform

from py2n import Py2NDevice, Py2NConnectionData

from .const import DOMAIN
from .coordinator import Helios2nPortDataUpdateCoordinator, Helios2nSwitchDataUpdateCoordinator

platforms = [Platform.BUTTON, Platform.LOCK, Platform.SWITCH, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, config: ConfigType) -> bool:
	aiohttp_session = async_get_clientsession(hass)
	connection_data = Py2NConnectionData(host= config.data[CONF_HOST], username=config.data[CONF_USERNAME], password=config.data[CONF_PASSWORD])
	device = await Py2NDevice.create(aiohttp_session, connection_data)
	hass.data.setdefault(DOMAIN,{})[config.entry_id] = device
	for platform in platforms:
		hass.data[DOMAIN].setdefault(platform, {})
	hass.data[DOMAIN][Platform.LOCK]["coordinator"] = Helios2nSwitchDataUpdateCoordinator(hass, device)
	hass.data[DOMAIN][Platform.SWITCH]["coordinator"] = Helios2nPortDataUpdateCoordinator(hass, device)
	hass.data[DOMAIN][Platform.BINARY_SENSOR]["coordinator"] = Helios2nPortDataUpdateCoordinator(hass, device)
	hass.async_create_task(
		hass.config_entries.async_forward_entry_setups(
		config, platforms
		)
	)
	return True