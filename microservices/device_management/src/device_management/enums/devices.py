from enum import StrEnum


class DeviceActivityStatuses(StrEnum):
    On = "on"
    Off = "off"


class DeviceInstallationStatuses(StrEnum):
    Active = "active"
    Inactive = "inactive"
