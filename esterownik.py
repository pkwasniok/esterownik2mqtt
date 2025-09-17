from dataclasses import dataclass
import requests
import json
import struct


@dataclass
class EsterownikTemperatures:
    exhaust: float
    domestic_water: float
    technic_water_input: float
    technic_water_output: float
    feeder: float
    outdoor: float
    indoor_a: float
    indoor_b: float


@dataclass
class EsterownikStatus:
    mode: int
    feeder_enabled: bool
    blower_enabled: bool
    pump_domestic_water_enabled: bool
    pump_technic_water_a_enabled: bool
    pump_technic_water_b_enabled: bool
    temperatures: EsterownikTemperatures


class Esterownik:
    address: str
    username: str
    password: str

    def __init__(self, address: str, username: str, password: str) -> None:
        self.address = address
        self.username = username
        self.password = password

    def request(self, payload: str) -> bytes:
        url = f'http://{self.address}?com={payload}'
        auth = (self.username, self.password)

        response = requests.get(url, auth=auth)

        return bytes(json.loads(response.text))

    def get_status(self) -> EsterownikStatus:
        response = self.request('02010006000000006103')

        temperatures = EsterownikTemperatures(
                exhaust = struct.unpack('<h', response[30:32])[0] / 10,
                domestic_water = struct.unpack('<h', response[22:24])[0] / 10,
                technic_water_input = struct.unpack('<h', response[24:26])[0] / 10,
                technic_water_output = struct.unpack('<h', response[28:30])[0] / 10,
                feeder = struct.unpack('<h', response[26:28])[0] / 10,
                outdoor = struct.unpack('<h', response[20:22])[0] / 10,
                indoor_a = struct.unpack('<h', response[18:20])[0] / 10,
                indoor_b = struct.unpack('<h', response[16:18])[0] / 10)

        return EsterownikStatus(
                mode = response[34],
                blower_enabled = bool(response[32] & (1 << 0)),
                feeder_enabled = bool(response[32] & (1 << 1)),
                pump_domestic_water_enabled = bool(response[32] & (1 << 3)),
                pump_technic_water_a_enabled = bool(response[32] & (1 << 2)),
                pump_technic_water_b_enabled = bool(response[32] & (1 << 4)),
                temperatures=temperatures)

