from ..exceptions import HomeException

class SceneNotFoundException(HomeException):
    def __init__(self, scene: str) -> None:
        self.message = f"The requested scene '{scene}' was not found in the list of scenes."
        super().__init__()