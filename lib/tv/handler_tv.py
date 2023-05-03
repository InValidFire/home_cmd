import urllib.parse

import requests

from lib.exceptions import DeviceNotFoundException
from .tv_device import TV

class TVHandler:
    def discover_tvs(self) -> list[TV]:
        tvs = []
        rokus = TV.discover()
        for roku in rokus:
            try:
                roku = TV.load_from_ip(roku.host)
            except DeviceNotFoundException:
                identifier = input(f"Found new roku '{roku.host}', what would you like to name it? ")
                roku = TV.from_roku(roku, identifier)
                roku.save()
            tvs.append(roku)
        return tvs

    def get_commands(self, identifier: str):
        tv = TV.load_from_identifier(identifier)
        return tv.commands

    def get_tvs(self):
        return TV.get_tvs()

    def open_app(self, identifier: str, app: str):
        tv = TV.load_from_identifier(identifier)
        app = tv[app]
        app.launch()

    def play_youtube(self, identifier: str, url: str):
        tv = TV.load_from_identifier(identifier)
        url = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(url.query)
        requests.post(f"http://{tv.host}:{tv.port}/launch/837?contentID={qs['v'][0]}", timeout=5)

    def toggle_mute(self, identifier: str):
        tv = TV.load_from_identifier(identifier)
        tv.volume_mute()

    def toggle_mute_all(self):
        for tv in TV.get_tvs():
            tv.voume_mute()

    def rename(self, identifier, new_identifier):
        tv = TV.load_from_identifier(identifier)
        tv.rename(new_identifier)