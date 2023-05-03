class HomeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class DeviceNotFoundException(HomeException):
    def __init__(self, identifier) -> None:
        self.message = f"The requested device '{identifier}' was not found in the home data."
        super().__init__()
