"""Support for monitoring an OpenEVSE Charger."""
import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import SENSOR_TYPES, COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the OpenEVSE sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    unique_id = entry.entry_id

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(OpenEVSESensor(sensor, unique_id, coordinator))

    async_add_entities(sensors, False)


class OpenEVSESensor(CoordinatorEntity):
    """Implementation of an OpenEVSE sensor."""

    def __init__(self, sensor_type, unique_id, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._name = SENSOR_TYPES[sensor_type][0]
        self._type = sensor_type
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self._icon = SENSOR_TYPES[sensor_type][3]
        self._unique_id = unique_id
        self._data = coordinator.data
        self._coordinator = coordinator

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return f"{self._name}_{self._unique_id}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        self._data = self._coordinator.data
        if self._data.data is None:
            return None
        if self._type in self._data.data.keys():
            if self._type == "charge_time":
                return self._data.data[self._type] / 60
            elif self._type == "usage_session":
                return self._data.data[self._type] / 1000
            elif self._type == "usage_total":
                return self._data.data[self._type] / 1000
            else:
                return self._data.data[self._type]
        return None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this sensor."""
        return self._unit_of_measurement

    @property
    def icon(self) -> str:
        """Return the unit of measurement."""
        return self._icon

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._coordinator.last_update_success
