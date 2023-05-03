from __future__ import annotations

from typing import Optional

import pywizlight
from pywizlight.bulb import wizlight, PORT

from .exceptions import SceneNotFoundException
from .lightdata import LightData


class Light(wizlight):
    ld = LightData()

    def __init__(self, ip: str, identifier: str = None, port: Optional[int] = PORT, mac: Optional[str] = None) -> None:
        self.identifier = identifier
        super().__init__(ip, port, mac)

    @classmethod
    def load_from_id(cls, identifier: str):
        ip = cls.ld.get_device_ip(identifier)
        return cls(ip, identifier)

    @classmethod
    def load_from_ip(cls, ip: str):
        identifier = cls.ld.get_device_identifier(ip)
        return cls(ip, identifier)

    @classmethod
    def from_wizlight(cls, light: wizlight, identifier: str):
        return cls(light.ip, identifier)

    @classmethod
    def get_lights(cls) -> list[Light]:
        lights = []
        for identifier in cls.ld.get_identifiers():
            lights.append(cls.load_from_id(identifier))
        return lights

    @classmethod
    def get_scenes(cls) -> dict[str, int]:
        SCENES = {value: key for key, value in pywizlight.SCENES.items()}
        return SCENES

    async def set_scene(self, scene: str):
        SCENES = Light.get_scenes()
        if scene not in SCENES:
            raise SceneNotFoundException(scene)
        await self.turn_on(pywizlight.PilotBuilder(scene=SCENES[scene]))

    async def set_brightness(self, level: int):
        await self.turn_on(pywizlight.PilotBuilder(brightness=255*(level/100)))

    def save(self):
        self.ld.save_device(self.ip, self.identifier)

    def rename(self, new_identifier):
        self.ld.rename_device(self.identifier, new_identifier)
