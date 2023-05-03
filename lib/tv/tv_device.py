from __future__ import annotations
from roku import Roku as RokuParent

from .tvdata import TVData

class TV(RokuParent):
    rd = TVData()

    def __init__(self, ip: str, identifier: str, port: int=8060):
        self.identifier = identifier
        super().__init__(ip, port)

    @classmethod
    def from_roku(cls, roku: RokuParent, identifier: str):
        return cls(roku.host, identifier)

    @classmethod
    def load_from_id(cls, identifier: str):
        ip = cls.rd.get_device_ip(identifier)
        return cls(ip, identifier)

    @classmethod
    def load_from_ip(cls, ip: str):
        identifier = cls.rd.get_device_identifier(ip)
        return cls(ip, identifier)

    @classmethod
    def get_tvs(cls) -> list[TV]:
        tvs = []
        for identifier in cls.rd.get_identifiers():
            tvs.append(cls.load_from_id(identifier))
        return tvs

    @classmethod
    def load_from_identifier(cls, identifier: str):
        ip = cls.rd.get_device_ip(identifier)
        return cls(ip, identifier)

    def save(self):
        self.rd.save_device(self.host, self.identifier)

    def rename(self, new_identifier):
        self.rd.rename_device(self.identifier, new_identifier)