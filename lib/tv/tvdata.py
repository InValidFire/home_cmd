from pathlib import Path
from ..homedata import HomeData

class TVData(HomeData):
    def __init__(self) -> None:
        self.path = Path.home().joinpath(".storage/roku.json")
