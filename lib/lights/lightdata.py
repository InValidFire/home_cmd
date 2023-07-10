from pathlib import Path

from ..homedata import HomeData

class LightData(HomeData):
    def __init__(self) -> None:
        self.path = Path.home().joinpath("storage/lights.json")

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value: Path):
        if isinstance(value, Path):
            value.parent.mkdir(parents=True, exist_ok=True)
            self._path = value
        else:
            raise TypeError(value)