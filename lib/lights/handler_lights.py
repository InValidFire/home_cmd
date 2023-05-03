from pywizlight import discovery

from ..exceptions import DeviceNotFoundException
from .light_device import Light

class LightHandler:
    async def discover_lights(self) -> list[Light]:
        lights = []
        bulbs = await discovery.discover_lights()
        for bulb in bulbs:
            try:
                light = Light.load_from_ip(bulb.ip)
            except DeviceNotFoundException:
                identifier = input(f"Found new light '{bulb.ip}', what would you like to name it? ")
                light = Light.from_wizlight(bulb, identifier)
                light.save()
            lights.append(light)
        return lights

    async def toggle_all(self):
        lights = Light.get_lights()
        for light in lights:
            await light.lightSwitch()
            await light.async_close()

    async def toggle(self, identifier: str):
        light = Light.load_from_id(identifier)
        await light.lightSwitch()
        await light.async_close()

    async def set_scene(self, identifier: str, scene: str):
        light = Light.load_from_id(identifier)
        await light.set_scene(scene)
        await light.async_close()

    async def set_scene_all(self, scene: str):
        lights = Light.get_lights()
        for light in lights:
            await light.set_scene(scene)
            await light.async_close()

    async def set_brightness(self, identifier: str, level: int):
        light = Light.load_from_id(identifier)
        await light.set_brightness(level)
        await light.async_close()

    async def set_brightness_all(self, level: int):
        lights = Light.get_lights()
        for light in lights:
            await light.set_brightness(level)
            await light.async_close()

    async def rename(self, identifier: str, new_identifier: str):
        light = Light.load_from_id(identifier)
        light.rename(new_identifier)

    def get_lights(self) -> list[Light]:
        return Light.get_lights()

    def get_scenes(self) -> list[str]:
        return Light.get_scenes()