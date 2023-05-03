import json
from pathlib import Path

from .exceptions import DeviceNotFoundException

class HomeData:
    def __new__(cls):  # singleton
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    @property
    def path(self):
        if not hasattr(self, '_path'):
            self._path = None
        return self._path

    @path.setter
    def path(self, new_path):
        if isinstance(new_path, Path):
            self._path = new_path
        else:
            raise TypeError(new_path)

    def _read_data_file(self) -> dict:
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True)
        if not self.path.exists():
            self.path.touch()
            self.path.write_text("{}")
        with self.path.open("r+", encoding="utf-8") as fp:
            data = json.load(fp)
        return data

    def _save_data_file(self, data):
        self.path.write_text(json.dumps(data, indent=4, sort_keys=True))

    def save_device(self, ip: str, identifier: str):
        data = self._read_data_file()
        if identifier not in data:
            data[identifier] = {}
        data[identifier]['ip'] = ip
        self._save_data_file(data)

    def get_device_ip(self, identifier: str):
        data = self._read_data_file()
        try:
            return data[identifier]['ip']
        except KeyError as exc:
            raise DeviceNotFoundException(identifier) from exc

    def get_device_identifier(self, ip: str):
        data = self._read_data_file()
        for device in data:
            if data[device]['ip'] == ip:
                return device
        raise DeviceNotFoundException(ip)

    def remove_device(self, identifier: str):
        data = self._read_data_file()
        data.pop(identifier)
        self._save_data_file(data)

    def rename_device(self, identifier: str, new_identifier: str):
        data = self._read_data_file()
        data[new_identifier] = data[identifier]
        data.pop(identifier)
        self._save_data_file(data)

    def get_identifiers(self) -> list[str]:
        data = self._read_data_file()
        identifiers = []
        for item in data.keys():
            identifiers.append(item)
        return identifiers