from pathlib import Path

from ..homedata import HomeData

class LightData(HomeData):
    def __init__(self) -> None:
        self.path = Path.home().joinpath(".storage/lights.json")
