from attrs import define
from typing import Optional


@define
class Hardware:
    name: str
    model: Optional[str] = ""
    manufacturer: Optional[str] = ""
    sw_version: Optional[str] = ""
    hw_version: Optional[str] = ""
    identifiers: Optional[list[str]] = ""
    connections: Optional[list[tuple]] = ""
    configuration_url: Optional[str] = ""
    via_device: Optional[str] = ""
